# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import random
import traceback
import uuid

import sentry_sdk
from pydash import get
from datetime import timedelta
from config import Config
from connect import dlm, redis_cluster
from enums.order import Status, Units
from exception import TxRecorded, TxPayment, ExPromoCodeInvalid, TxTimeout, ExCheckFiat
from helper.items import ItemsHelper
from helper.metadata import MetaDataHelper
from helper.simplex import SimplexHelper
from helper.socket import SocketEmitter
from lib import NotFound, dt_utcnow, BadRequest
from lib.logger import debug
from models import PaymentConfigModel, OrderModel, PromotionCodeModel, ReferralModel, BoxModel, \
    MeshMaterialModel
from tasks.order import task_record_tx


class OrderHelper:

    @staticmethod
    def convert_price_to_usdt(value, unit):
        _price = {}
        if unit == Units.ETH:
            _price = redis_cluster.get('katana-dapp.price_pairs/ETHBUSD')
        if unit == Units.BNB:
            _price = redis_cluster.get('katana-dapp.price_pairs/BNBBUSD')
        if _price:
            if isinstance(_price, str):
                _price = json.loads(_price)
            _check_time = dt_utcnow().timestamp() - 60 * 5  # Mint 5p
            if get(_price, 'updated_time', 0) < _check_time:
                sentry_sdk.capture_message("Price update failed")
                raise BadRequest(f"Can not check price of nft. From {unit} to USDT")
            return value / get(_price, 'price')
        return value

    @classmethod
    def get_cost_of(cls, item, unit):
        return float(cls.convert_price_to_usdt(get(item, 'price'), unit=unit))

    @staticmethod
    def get_item(item):
        _info = MeshMaterialModel.find_one({
            "nft_id": get(item, 'nft_id'),
        })
        if not _info:
            raise NotFound(msg='Not found item.')
        # if get(_info, 'contract') != contract:
        #     raise NotFound(msg='Not found item in the contract.')

        return {
            **_info,
            **ItemsHelper.get_info_of_mesh_material(get(_info, 'mesh_id'))
        }

    @staticmethod
    def get_box_item(item):

        item = BoxModel.find_one({
            'box_id': get(item, 'nft_id'),
        })

        if not item:
            raise NotFound(msg='Not found item.')

        return item

    @classmethod
    def promotion_code(cls, form_data, order_id):
        # if Config.DEBUG:
        #     return 0

        if get(form_data, 'promotion_code'):
            _promotion_code = get(form_data, 'promotion_code')

            _info = PromotionCodeModel.find_one({
                'code': _promotion_code
            })

            if get(_info, 'used') >= get(_info, 'total'):
                raise ExPromoCodeInvalid()

            _promotion_code_used = redis_cluster.get(f'katana-dapp.promotion_code_used/{_promotion_code}')

            if int(_promotion_code_used) >= get(_info, 'total'):
                raise ExPromoCodeInvalid()

            MetaDataHelper.update_used_promotion_code(
                promotion_code=_promotion_code,
                address=get(form_data, 'address').lower(),
                order_id=order_id,
                updated_by='order:promotion_code'
            )
            return get(_info, 'discount', 0)
        return 0

    @staticmethod
    def mockup_item(item, discount, ref_code_discount):
        _price = item['price'] * get(item, 'amount')
        _ref_discount = 0

        item['raw_price'] = _price

        if ref_code_discount:
            _ref_discount = get(item, 'discount', 0)

        _promotion_discount = _price * (discount / 100)

        _price = _price - _promotion_discount
        _referral_discount = _price * (_ref_discount / 100)
        _price = _price - _referral_discount

        # item['price'] = _price
        item['discount'] = item['raw_price'] - _price

        return {
            **item,
            'price': _price,
            'promotion_percent': _ref_discount,
            'promotion_discount': _promotion_discount,
            'referral_percent': _ref_discount,
            'referral_discount': _referral_discount,
            'price_after_discount': _price
        }

    @staticmethod
    def check_ref_code(ref_code):
        if ref_code:
            ref_code = ReferralModel.find_one({
                'code': ref_code
            }, cache=True)
            if not ref_code:
                raise BadRequest(msg=f"Not found ref code#{ref_code}")
            return True
        return False

    @classmethod
    def get_items(cls, form_data):
        if get(form_data, 'nft_type') == 'box':
            return [{**cls.get_box_item(_item), 'amount': get(_item, 'amount')}
                    for _item in get(form_data, 'items')]
        else:
            return [{
                **cls.get_item(_item),
                'amount': get(_item, 'amount')
            }
                for _item in get(form_data, 'items')]

    @classmethod
    def init(cls, form_data):

        _order_id = str(uuid.uuid4())

        _address_of_counter = ''

        _payment_id = ''

        _fiat = 0

        _discount = cls.promotion_code(form_data, order_id=_order_id)

        _simplex = {

        }

        _ref_code_discount = cls.check_ref_code(get(form_data, 'ref_code'))

        _items = [cls.mockup_item({
            # **cls.get_item(_item, get(form_data, 'contract').lower()),
            **_item,
            'amount': get(_item, 'amount')
        }, discount=_discount, ref_code_discount=_ref_code_discount) for _item in cls.get_items(form_data)]

        _deadline = dt_utcnow().timestamp() + 3 * 60
        # Price to USDT

        _cost = sum([cls.get_cost_of(_item, unit=get(form_data, 'unit')) for _item in _items])

        if Units.FIAT == get(form_data, 'unit'):

            _payment_id = _order_id

            _res = SimplexHelper.quote(
                end_user_id=_payment_id,
                amount=_cost
            )

            if not _res:
                raise ExCheckFiat

            _simplex = _res

            _fiat = get(_simplex, 'fiat_money.total_amount')

        else:

            _address_of_counter = get(random.choice(PaymentConfigModel.find(
                filter={
                    'chain': get(form_data, "chain")
                })), 'address')

        OrderModel.insert_one({
            'address': get(form_data, 'address').lower(),
            'order_id': _order_id,
            'cost': _cost,
            'discount': _discount,
            'items': _items,
            'address_of_counter': _address_of_counter,
            'created_by': get(form_data, 'address'),
            'status': Status.WAITING_FOR_PAYMENT,
            'deadline': _deadline,
            'chain': get(form_data, 'chain', ''),
            'unit': get(form_data, 'unit'),
            'contract': get(_items[0], 'address').lower(),
            'ref_code': get(form_data, 'ref_code'),
            'payment_id': _payment_id,
            'simplex': _simplex,
            'fiat': _fiat,
            'nft_type': get(form_data, 'nft_type', 'raw_nft')
        }, worker=False)

        return {
            'order_id': _order_id,
            'cost': _cost,
            'discount': _discount,
            'address_of_counter': _address_of_counter or '',
            'unit': get(form_data, 'unit'),
            'chain': get(form_data, 'chain'),
            'deadline': _deadline,
            'fiat': _fiat
        }

    @staticmethod
    def lock_tx(chain, tx_hash):
        # return True
        if Config.DEBUG:
            return True
        try:
            _lock = dlm.lock(f'ktn:logs:tx_hash:{chain}:{tx_hash}', 60 * 1 * 1000)
            if _lock:
                debug(f'[EVENT] \033[92m ✔✔✔ Process .................. {tx_hash} \033[0m')
                return True
            else:
                debug(f'[EVENT] \033[93m ⚠⚠⚠ ______ Lock fail ______ {tx_hash} \033[0m')
        except:
            traceback.print_exc()
            sentry_sdk.capture_exception()
        return False

    @classmethod
    def make_payment(cls, form_data):
        _tx_hash = get(form_data, 'tx_hash')
        _tx_hash = _tx_hash.lower()
        if not cls.lock_tx(get(form_data, 'chain'), get(form_data, 'tx_hash')):
            raise TxRecorded()
        _order = OrderModel.find_one({
            'order_id': get(form_data, 'order_id')
        })
        if not _order:
            raise NotFound(msg="Not found order.")
        if get(_order, 'status') != Status.WAITING_FOR_PAYMENT:
            raise TxPayment()
        if get(_order, 'deadline') < dt_utcnow().timestamp():
            raise TxTimeout()

        task_record_tx.delay(
            tx_hash=_tx_hash,
            order_id=get(form_data, 'order_id')
        )

        return {
            'tx_hash': _tx_hash,
            'order_id': get(form_data, 'order_id'),
            'status': Status.CHECKING
        }

    @staticmethod
    def on_minted(address, order_id, token_ids, tx_hash):
        OrderModel.update_one({
            'order_id': order_id
        }, obj={
            'updated_by': 'on_minted',
            'token_ids': token_ids,
            'tx_mint': tx_hash,
            'status': Status.DONE
        })
        SocketEmitter.emit(
            room_id=address,
            event='ORDER_STEP',
            value={
                'order_id': order_id,
                'token_ids': token_ids,
                'tx_mint': tx_hash,
                'status': Status.DONE
            }
        )
        return "Done"
