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
from exception import TxRecorded, TxPayment, ExPromoCodeInvalid, TxTimeout
from helper.socket import SocketEmitter
from lib import NotFound, dt_utcnow, BadRequest
from lib.logger import debug
from models import NFTDetailModel, PaymentConfigModel, OrderModel, PromotionCodeModel
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
        return float(cls.convert_price_to_usdt(get(item, 'price'), unit=unit) * get(item, 'amount'))

    @staticmethod
    def get_item(item):
        _info = NFTDetailModel.find_one({
            "nft_id": get(item, 'nft_id')
        })

        if not _info:
            raise NotFound(msg='Not found item.')

        return _info

    @classmethod
    def promotion_code(cls, form_data):
        # if Config.DEBUG:
        #     return 0

        if get(form_data, 'promotion_code'):

            if not cls.lock_promo_code(get(form_data, 'promotion_code')):
                raise ExPromoCodeInvalid(msg="The promo code has been used.")

            _info = PromotionCodeModel.find_one({
                'code': get(form_data, 'promotion_code')
            })
            if not get(_info, 'status'):
                raise ExPromoCodeInvalid()
            return get(_info, 'discount', 0)
        return 0

    @classmethod
    def init(cls, form_data):
        _order_id = str(uuid.uuid4())
        _discount = cls.promotion_code(form_data)

        _items = [{
            **cls.get_item(_item),
            'amount': get(_item, 'amount')
        } for _item in get(form_data, 'items')]
        _deadline = dt_utcnow().timestamp() + 3 * 60
        _cost = sum([cls.get_cost_of(_item, unit=get(form_data, 'unit')) for _item in _items]) - _discount

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
            'chain': get(form_data, 'chain'),
            'unit': get(form_data, 'unit'),
            'contract': Config.NFT_ADDRESS.lower()
        }, worker=True)

        return {
            'order_id': _order_id,
            'cost': _cost,
            'discount': _discount,
            'address_of_counter': _address_of_counter or '',
            'unit': get(form_data, 'unit'),
            'chain': get(form_data, 'chain'),
            'deadline': _deadline
        }

    @staticmethod
    def lock_promo_code(code):
        try:
            _lock = dlm.lock(f'ktn:hot_lock:promo_codes:{code}', 3 * 60 * 1000)
            if _lock:
                debug(f'[EVENT] \033[92m ✔✔✔ Process .................. {code} \033[0m')
                return True
            else:
                debug(f'[EVENT] \033[93m ⚠⚠⚠ ______ Lock fail ______ {code} \033[0m')
        except:
            traceback.print_exc()
            sentry_sdk.capture_exception()
        return False

    @staticmethod
    def lock_tx(chain, tx_hash):
        # return True
        if Config.DEBUG:
            return True
        try:
            _lock = dlm.lock(f'ktn:logs:tx_hash:{chain}:{tx_hash}', 60 * 10 * 1000)
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
            'tx_hash': tx_hash,
            'status': Status.DONE
        })
        SocketEmitter.emit(
            room_id=address,
            event='ORDER_STEP',
            value={
                'order_id': order_id,
                'token_ids': token_ids,
                'tx_hash': tx_hash,
                'status': Status.DONE
            }
        )
        return "Done"
