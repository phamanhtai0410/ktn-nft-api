import uuid

import web3
from flask_restful import Resource
from pydash import get

from config import Config
from connect import security
from exceptions.metadata import CollectionNotFoundEx
from helper.mesh import MeshHelper
from helper.metadata import MetaDataHelper
from lib import dt_utcnow, NotFound
from models import SignatureLogModel, CollectionModel
from schemas.metadata import MetaDataSchema, ResMetaDataSchema
from lib.logger import debug

DISCOUNT_DECIMALS = 10 ** 18


class MetaDataResource(Resource):

    @security.http(
        form_data=MetaDataSchema(),
        response=ResMetaDataSchema()
    )
    async def post(self, form_data):

        _chain_id = get(form_data, 'chain_id')
        _address = get(form_data, 'address').lower()
        _promotion_code = get(form_data, 'promotion_code')
        _ref_code = get(form_data, 'ref_code')
        _items = get(form_data, 'items')
        _collection_address = get(form_data, 'collection_address')
        # FIXME: check flow whitelist in BE later
        _is_whitelist_mint = False

        _promotion_discount_percent = MetaDataHelper.promotion_discount_percent(promotion_code=_promotion_code)
        _promotion_discount_total = 0
        _referral_code_checked = MetaDataHelper.referral_discount_percent(ref_code=_ref_code, address=_address)
        _referral_discount_total = 0

        _collection = None
        _items_discount = []

        for _nft_index in _items:
            # _mesh_material_detail = MeshHelper.get_mesh_material_by_nft_id(_item)
            # if _mesh_material_detail is None:
            #     debug(f'Nft id: {_item} not found in mesh_materials collection.')
            #     raise NotFound(msg='Nft id not found.')

            # _mesh_id = get(_mesh_material_detail, 'mesh_id')
            # _mesh_detail = MeshHelper.get_mesh_by_id(mesh_id=_mesh_id)
            # if _mesh_detail is None:
            #     debug(f'Mesh id: {_mesh_id} not found in meshes collection.')
            #     raise NotFound(msg='Mesh id not found.')
            _collection = CollectionModel.find_one({
                'address': _collection_address,
                'chain_id': _chain_id
            })
            if not _collection:
                debug(f'Collection address: {_collection_address}')
                raise CollectionNotFoundEx

            _price = float(get(_collection, f'types_list.{_nft_index}.price', 0))
            _promotion_discount_item = _price * (_promotion_discount_percent / 100)
            _promotion_discount_total += _promotion_discount_item

            _referral_discount_percent = 0
            _referral_discount_item = 0

            if _referral_code_checked:
                _referral_discount_percent = get(_collection, 'discount', 0)

                _referral_discount_item = (_price - _promotion_discount_item) * (_referral_discount_percent / 100)

                _referral_discount_total += _referral_discount_item

            _discount_data = {
                'nft_id': _nft_index,
                'commission': get(_collection, 'commission', 0),
                'commission_level_2': get(_collection, 'commission_level_2', 0),
                'promotion_percent': _promotion_discount_percent,
                'promotion_discount': _promotion_discount_item,
                'referral_percent': _referral_discount_percent,
                'referral_discount': _referral_discount_item,
                'raw_price': _price,
                'price_after_discount': _price - _promotion_discount_item - _referral_discount_item
            }

            _items_discount.append(_discount_data)

        _log_id = str(uuid.uuid4())
        SignatureLogModel.insert_one({
            'log_id': _log_id,
            'address': _address.lower(),
            'collection': _collection,
            'ref_code': _ref_code,
            'promotion_code': _promotion_code,
            'items': _items_discount,
            'is_whitelist_mint': _is_whitelist_mint,
            'created_by': 'metadata_api',
            'created_time': dt_utcnow()
        })

        _deadline = dt_utcnow().timestamp() + 60 * 60
        _discount = web3.Web3.toWei((_promotion_discount_total + _referral_discount_total), 'ether')

        #NOTE: contract for sign will get from collection for multichain
        _dapp_creator_address = get(_collection, 'dapp_creator_address')
        _data = {
            'chain_id': _chain_id,
            'address': web3.Web3.toChecksumAddress(_address),
            'contract': web3.Web3.toChecksumAddress(_dapp_creator_address),
            'collection': web3.Web3.toChecksumAddress(_collection_address),
            'discount': _discount,
            'is_whitelist_mint': _is_whitelist_mint,
            'nft_indexes': _items,
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
                'nft_indexes': _items,
                'collection_address': str(get(_data, 'collection')),
                'is_whitelist_mint': _is_whitelist_mint,
                'deadline': get(_data, 'deadline'),
            },
            'signature': _signature,
            'callback': _log_id
        }
