import json

from flask_restful import Resource
from pydash import get

from config import Config
from connect import security
from helper.ipfs import IPFSHelper
from helper.metadata import MetaDataHelper
from lib import dt_utcnow
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
            _metadata = {
                "description": get(_item, 'description'),
                "external_url": "",
                "image": get(_item, 'image'),
                "rarity": get(_item, 'rarity'),
                "name": get(_item, 'name')
            }
            _cid = IPFSHelper.upload_web3(metadata=_metadata)
            _cids_bytes.append(bytes(_cid, 'utf-8'))
            _cids.append(_cid)
            _rarities.append(get(_item, 'rarity'))
            _types.append(get(_item, 'type'))

        _deadline = dt_utcnow().timestamp() + 60
        _data = {
            'address': _address,
            'contract': Config.NFT_ADDRESS,
            'discount': _discount,
            'cids_bytes': _cids_bytes,
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
            'signature': str(_signature)
        }
