from flask_restful import Resource
from pydash import get

from config import Config
from connect import security
from exception import ExRefCodeInvalid, ExRefCodeOwner
from helper.ipfs import IPFSHelper
from helper.items import ItemsHelper
from helper.metadata import MetaDataHelper
from lib import dt_utcnow, NotFound
from models import ReferralModel
from schemas.metadata import MetaDataSchema, ResMetaDataSchema

DISCOUNT_DECIMALS = 10 ** 18


class MetaDataResource(Resource):

    @security.http(
        form_data=MetaDataSchema(),
        response=ResMetaDataSchema()
    )
    def post(self, form_data):

        _address = get(form_data, 'address')
        _promotion_code = get(form_data, 'promotion_code')
        _ref_code = get(form_data, 'ref_code')
        _items = get(form_data, 'items')

        _is_have_ref_code = False
        if _ref_code is not None:
            _referral = ReferralModel.find_one({
                'code': _ref_code
            })

            if _referral is None:
                raise ExRefCodeInvalid()
            if get(_referral, 'address') == _address:
                raise ExRefCodeOwner()
            _is_have_ref_code = True

        _promotion_discount = MetaDataHelper.discount(promotion_code=_promotion_code)
        _referral_discount = 0

        _cids = []
        _cids_bytes = []
        _rarities = []
        _types = []
        for _item in _items:
            _nft_detail = ItemsHelper.get_item_by_id(_item)
            if _nft_detail is None:
                raise NotFound(msg='Not found nft id.')

            if _is_have_ref_code:
                _price = get(_nft_detail, 'price')
                _discount_percent = get(_nft_detail, 'discount')
                _referral_discount += round(_price * (_discount_percent / 100), 2)

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
            _cid = IPFSHelper.upload_web3(metadata=_metadata)
            _cids.append(_cid)
            _rarities.append(get(_nft_detail, 'rarity'))
            _types.append(get(_nft_detail, 'type'))

        _deadline = dt_utcnow().timestamp() + 60 * 60
        _discount = int((_promotion_discount + _referral_discount) * DISCOUNT_DECIMALS)
        _data = {
            'address': _address,
            'contract': Config.NFT_ADDRESS,
            'discount': _discount,
            'cids': _cids,
            'types': _types,
            'rarities': _rarities,
            'deadline': int(_deadline)
        }
        _signature = MetaDataHelper.generate_signature(data=_data)

        return {
            'data': {
                'discount': get(_data, 'discount'),
                'cids': get(_data, 'cids'),
                'types': get(_data, 'types'),
                'rarities': get(_data, 'rarities'),
                'deadline': get(_data, 'deadline'),
            },
            'signature': _signature
        }
