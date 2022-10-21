import web3

from flask_restful import Resource
from pydash import get

from config import Config
from connect import security
from helper.ipfs import IPFSHelper
from helper.items import ItemsHelper
from helper.metadata import MetaDataHelper
from lib import dt_utcnow, NotFound
from schemas.metadata import MetaDataSchema, ResMetaDataSchema


class MetaDataResource(Resource):

    @security.http(
        form_data=MetaDataSchema(),
        response=ResMetaDataSchema()
    )
    def post(self, form_data):

        _address = get(form_data, 'address')
        _promotion_code = get(form_data, 'promotion_code')
        _items = get(form_data, 'items')

        _discount = MetaDataHelper.discount(promotion_code=_promotion_code)

        _cids = []
        _cids_bytes = []
        _rarities = []
        _types = []
        for _item in _items:
            _nft_detail = ItemsHelper.get_item(
                filter_data={
                    'nft_id': _item,
                }
            )
            if _nft_detail is None:
                raise NotFound(msg='Not found nft id.')
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

        _deadline = dt_utcnow().timestamp() + 60
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
