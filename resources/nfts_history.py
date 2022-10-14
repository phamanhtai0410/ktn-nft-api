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
from schemas.nfts_history import NFTsHistoryRequestParams, NFTsHistoryResponseSchema


class NFTsHistoryResource(Resource):

    @security.http(
        params= NFTsHistoryRequestParams(),
        response=NFTsHistoryResponseSchema()
    )
    def get(self,params):
        _token_id = get(params, 'token_id')
        res = NFTsHistoryHelper.get_history(_token_id)
        return res
