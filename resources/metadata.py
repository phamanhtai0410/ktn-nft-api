import asyncio
import uuid

import web3
from flask_restful import Resource
from pydash import get

from config import Config
from connect import security
from helper.ipfs import IPFSHelper
from helper.items import ItemsHelper
from helper.metadata import MetaDataHelper
from lib import dt_utcnow, NotFound, BadRequest
from models import SignatureLogModel
from schemas.metadata import MetaDataSchema, ResMetaDataSchema
from lib.logger import debug

DISCOUNT_DECIMALS = 10 ** 18


class MetaDataResource(Resource):

    @security.http(
        form_data=MetaDataSchema(),
        response=ResMetaDataSchema()
    )
    async def post(self, form_data):

        _address = get(form_data, 'address').lower()
        _promotion_code = get(form_data, 'promotion_code')
        _ref_code = get(form_data, 'ref_code')
        _items = get(form_data, 'items')

        _promotion_discount_percent = MetaDataHelper.promotion_discount_percent(promotion_code=_promotion_code)
        _promotion_discount = 0
        _referral_code_checked = MetaDataHelper.referral_discount_percent(ref_code=_ref_code, address=_address)
        _referral_discount = 0

        _cids = []
        _metadata_list = []
        _rarities = []
        _types = []
        _items_discount = []
        for _item in _items:
            _nft_detail = ItemsHelper.get_item_by_id(_item)
            if _nft_detail is None:
                raise NotFound(msg='Not found nft id.')

            _price = get(_nft_detail, 'price', 0)

            _promotion_discount_item = _price * (_promotion_discount_percent / 100)
            _promotion_discount += _promotion_discount_item

            _referral_discount_percent = 0
            _referral_discount_item = 0

            if _referral_code_checked:
                _referral_discount_percent = get(_nft_detail, 'discount')

                _referral_discount_item = (_price - _promotion_discount_item) * (_referral_discount_percent / 100)

                _referral_discount += _referral_discount_item

            _discount_data = {
                'nft_id': _item,
                'rarity': get(_nft_detail, 'rarity'),
                'type': get(_nft_detail, 'type'),
                'commission_percent': get(_nft_detail, 'commission'),
                'promotion_percent': _promotion_discount_percent,
                'promotion_discount': _promotion_discount_item,
                'referral_percent': _referral_discount_percent,
                'referral_discount': _referral_discount_item,
                'raw_price': _price,
                'price_after_discount': _price - _promotion_discount - _referral_discount
            }

            _items_discount.append(_discount_data)

            _metadata = {
                "description": get(_nft_detail, 'description'),
                "external_url": "",
                "image": get(_nft_detail, 'image'),
                "name": get(_nft_detail, 'name'),
                'attributes': [
                    {
                        "display_type": "number",
                        "trait_type": "rarity",
                        "value": get(_nft_detail, 'rarity')
                    },
                    {
                        "display_type": "number",
                        "trait_type": "type",
                        "value": get(_nft_detail, 'type')
                    }
                ]
            }
            _metadata_list.append(_metadata)
            _rarities.append(get(_nft_detail, 'rarity'))
            _types.append(get(_nft_detail, 'type'))

        try:
            _cids = await asyncio.gather(
                *[IPFSHelper.upload_web3_async(metadata) for metadata in _metadata_list]
            )
        except Exception as e:
            debug(f'W3 storage exception: {e}')
            raise BadRequest(msg="W3 storage rate limit.")

        _log_id = str(uuid.uuid4())
        SignatureLogModel.insert_one({
            'log_id': _log_id,
            'address': _address.lower(),
            'ref_code': _ref_code,
            'promotion_code': _promotion_code,
            'items': _items_discount,
            'created_by': 'metadata_api',
            'created_time': dt_utcnow()
        })

        _deadline = dt_utcnow().timestamp() + 60 * 60
        _discount = web3.Web3.toWei((_promotion_discount + _referral_discount), 'ether')
        _data = {
            'address': web3.Web3.toChecksumAddress(_address),
            'contract': web3.Web3.toChecksumAddress(Config.CREATOR_ADDRESS),
            'discount': _discount,
            'cids': _cids,
            'types': _types,
            'rarities': _rarities,
            'deadline': int(_deadline)
        }
        debug(f'Sign data: {_data}')
        _signature = MetaDataHelper.generate_signature(data=_data)
        MetaDataHelper.update_used_promotion_code(
            promotion_code=_promotion_code,
            address=_address.lower(),
            updated_by='metadata:update_used_promotion_code'
        )

        return {
            'data': {
                'discount': str(get(_data, 'discount')),
                'cids': get(_data, 'cids'),
                'types': get(_data, 'types'),
                'rarities': get(_data, 'rarities'),
                'deadline': get(_data, 'deadline'),
            },
            'signature': _signature,
            'callback': _log_id
        }
