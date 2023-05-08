# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from helper.my_nfts import MyNFTsHelpers
from schemas.forging_list import ForgingListRequestSchema, ForgingListResponseSchema


class ForgingListResource(Resource):

    @security.http(
        params=ForgingListRequestSchema(),
        response=ForgingListResponseSchema()
    )
    def get(self, params):
        # _query = request.args.to_dict()
        _address = get(params, 'address').lower()
        _chain = get(params, 'chain')
        _collection_type = get(params, 'collection_type')
        _my_nfts = MyNFTsHelpers.get_forging_list(address=_address, chain=_chain, collection_type=_collection_type)

        return _my_nfts
