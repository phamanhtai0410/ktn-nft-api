# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get
from helper.items import ItemsHelper

from connect import security
from schemas.items import ItemRequestParams, ItemsListResponseSchema, ItemResponseSchema, ItemsListRequestSchema


class ItemsListResource(Resource):

    @security.http(
        params=ItemsListRequestSchema(),
        response=ItemsListResponseSchema()
    )
    def get(self,params):
        _nft_id = get(params , 'nft_id')
        _type = get(params, 'type')
        _page= get(params, 'page')
        _page_size = get(params, 'page_size')
        res = ItemsHelper.get_items(_nft_id, _type, _page, _page_size)
        return res



