# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get
from connect import security
from flask import request

from helper.my_nfts import MyNFTsHelpers
from schemas.my_nfts import MyNFTsResponseSchema, MyNFTsRequestSchema


class MyNFTsResource(Resource):

    @security.http(
        params=MyNFTsRequestSchema(),
        response=MyNFTsResponseSchema()
    )
    def get(self, params):
        _query = request.args.to_dict()

        _page = get(params, 'page')
        _limit = get(params, 'limit')
        _address = get(params, 'address')
        _arrange = get(params, 'arrange').lower() == 'asc' and 1 or -1

        _offset = _page > 0 and (_page - 1) * _limit or 0

        _my_nfts = MyNFTsHelpers.get_my_nfts(address=_address, limit=_limit, offset=_offset, arrange=_arrange)

        return {
            'my_nfts': _my_nfts,
            'skip': _offset
        }
