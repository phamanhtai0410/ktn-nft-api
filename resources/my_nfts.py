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

        _page = get(params, 'page', default=1)
        _page_size = get(params, 'page_size', default=10)
        _address = get(params, 'address')
        _sort = get(params, 'sort').lower() == 'asc' and 1 or -1

        _my_nfts = MyNFTsHelpers.get_my_nfts(address=_address, page=_page, page_size=_page_size, sort=_sort)

        return _my_nfts
