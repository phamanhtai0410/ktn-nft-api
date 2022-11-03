# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get
from helper.nfts_history import NFTsHistoryHelper

from connect import security
from schemas.nfts_history import NFTsHistoryRequestParams, NFTsHistoryListResponseSchema


class NFTsHistoryResource(Resource):

    @security.http(
        params= NFTsHistoryRequestParams(),
        response=NFTsHistoryListResponseSchema()
    )
    def get(self,params):
        _token_id = get(params, 'token_id')
        _page = get(params, 'page')
        _page_size = get(params, 'page_size')
        _sort = get(params, 'sort').lower() == 'asc' and 1 or -1
        res = NFTsHistoryHelper.get_history(_token_id, _page, _page_size, _sort)
        return res
