# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import uuid

from flask_restful import Resource
from pydash import get

from config import Config
from connect import security, redis_cluster
from helper.forging import ForgingHelpers
from lib import dt_utcnow
from models import ForgingLogsModel
from schemas.forging_signature import ForgingSignatureRequestSchema, ForgingSignatureResponseSchema


class ForgingSignatureResource(Resource):
    @security.http(
        form_data=ForgingSignatureRequestSchema(),
        response=ForgingSignatureResponseSchema(),
    )
    def post(self, form_data):
        _chain_id = get(form_data, 'chain_id')
        _user_address = get(form_data, 'user_address', '').lower()
        _collection_address = get(form_data, 'collection_address', '').lower()
        _collection_addresses_forging = get(form_data, 'collection_addresses_forging', [])
        _token_ids_forging = get(form_data, 'token_ids_forging', [])
        _nft_indexes_forging = get(form_data, 'nft_indexes_forging', [])

        # Add nonce for limit order
        _key = f'katana-dapp.forging_signature/nonce'
        _nonce = redis_cluster.incr(name=_key, amount=1)

        _log_id = str(uuid.uuid4())
        ForgingLogsModel.insert_one({
            'log_id': _log_id,
            'nonce': _nonce,
            'chain_id': _chain_id,
            'user_address': _user_address,
            'collection_address': _collection_address,
            'collection_addresses_forging': _collection_addresses_forging,
            'token_ids_forging': _token_ids_forging,
            'nft_indexes_forging': _nft_indexes_forging,
            'created_by': 'ktn-nft-api:resources:forging_signature',
            'created_time': dt_utcnow()
        })
        _deadline = dt_utcnow().timestamp() + Config.SIGNATURE_EXPIRE_TIME

        _data = {
            'chain_id': _chain_id,
            'nonce': _nonce,
            'user_address': _user_address,
            'forging_address': '',  # Forging address get from DB
            'collection_address': _collection_address,
            'collection_addresses_forging': _collection_addresses_forging,
            'token_ids_forging': _token_ids_forging,
            'nft_indexes_forging': _nft_indexes_forging,
            'deadline': _deadline
        }

        _signature = ForgingHelpers.generate_signature(data=_data)

        return {
            'data': {
                **_data
            },
            'signature': _signature,
            'callback': _log_id
        }
