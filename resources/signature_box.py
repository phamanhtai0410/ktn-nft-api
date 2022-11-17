import uuid

import web3
from flask_restful import Resource
from pydash import get

from config import Config
from connect import security
from helper.box import BoxHelper
from helper.metadata import MetaDataHelper
from lib import dt_utcnow, NotFound
from models import SignatureLogModel
from schemas.signature_box import SignatureBoxSchema, ResSignatureBoxSchema
from lib.logger import debug

DISCOUNT_DECIMALS = 10 ** 18


class SignatureBoxResource(Resource):

    @security.http(
        form_data=SignatureBoxSchema(),
        response=ResSignatureBoxSchema()
    )
    async def post(self, form_data):

        _address = get(form_data, 'address').lower()
        _promotion_code = get(form_data, 'promotion_code')
        _ref_code = get(form_data, 'ref_code')
        _amount = get(form_data, 'amount')

        _promotion_discount_percent = MetaDataHelper.promotion_discount_percent(promotion_code=_promotion_code)
        _promotion_discount_total = 0
        _referral_code_checked = MetaDataHelper.referral_discount_percent(ref_code=_ref_code, address=_address)
        _referral_discount_total = 0

        _box_detail = BoxHelper.active()
        if _box_detail is None:
            raise NotFound(msg='Not found nft box.')

        _price = get(_box_detail, 'price', 0)

        _promotion_discount_item = _price * (_promotion_discount_percent / 100)
        _promotion_discount_total = _promotion_discount_item * _amount

        _referral_discount_percent = 0
        _referral_discount_item = 0

        if _referral_code_checked:
            _referral_discount_percent = get(_box_detail, 'discount')

            _referral_discount_item = (_price - _promotion_discount_item) * (_referral_discount_percent / 100)

            _referral_discount_total = _referral_discount_item * _amount

        _discount_data = {
            'amount': _amount,
            'commission': get(_box_detail, 'commission'),
            'commission_level_2': get(_box_detail, 'commission_level_2'),
            'promotion_percent': _promotion_discount_percent,
            'promotion_discount': _promotion_discount_total,
            'referral_percent': _referral_discount_percent,
            'referral_discount': _referral_discount_total,
            'raw_price': _price * _amount,
            'price_after_discount': _price * _amount - _promotion_discount_total - _referral_discount_total
        }

        _log_id = str(uuid.uuid4())
        SignatureLogModel.insert_one({
            'log_id': _log_id,
            'address': _address.lower(),
            'collection': get(_box_detail, 'address'),
            'ref_code': _ref_code,
            'promotion_code': _promotion_code,
            'items': [_discount_data],
            'created_by': 'signature_box_api',
            'created_time': dt_utcnow()
        })

        _deadline = dt_utcnow().timestamp() + 60 * 60
        _discount = web3.Web3.toWei((_promotion_discount_total + _referral_discount_total), 'ether')
        _data = {
            'address': web3.Web3.toChecksumAddress(_address),
            'contract': web3.Web3.toChecksumAddress(Config.BOX_CREATOR_CONTRACT),
            'collection': web3.Web3.toChecksumAddress(get(_box_detail, 'address')),
            'discount': _discount,
            'amount': _amount,
            'deadline': int(_deadline)
        }
        debug(f'Sign data: {_data}')
        _signature = BoxHelper.generate_signature(data=_data)
        MetaDataHelper.update_used_promotion_code(
            promotion_code=_promotion_code,
            address=_address.lower(),
            updated_by='signature_box:update_used_promotion_code'
        )

        return {
            'data': {
                'discount': str(get(_data, 'discount')),
                'collection': get(_data, 'collection'),
                'deadline': get(_data, 'deadline'),
            },
            'signature': _signature,
            'callback': _log_id
        }
