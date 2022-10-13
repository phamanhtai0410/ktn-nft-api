import json

from flask_restful import Resource
from pydash import get

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

        _promotion_code = get(form_data, 'promotion_code')
        _items = get(form_data, 'items')

        _discount = MetaDataHelper.discount(promotion_code=_promotion_code)

        _cids = []
        for _item in _items:
            _metadata = {
                "description": get(_item, 'description'),
                "external_url": "",
                "image": get(_item, 'image'),
                "rarity": get(_item, 'rarity'),
                "name": get(_item, 'name')
            }
            _cid = IPFSHelper.upload_web3(metadata=_metadata)
            _cids.append(_cid)

        _deadline = dt_utcnow().timestamp() + 60
        _data = {
            'chain_id': 97,
            'discount': _discount,
            'cids': _cids,
            'items': json.dumps(_items),
            'deadline': int(_deadline)
        }
        _signature = MetaDataHelper.generate_signature(data=_data)

        return {
            'data': _data,
            'signature': str(_signature)
        }
