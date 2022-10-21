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
from schemas.items import ItemsListResponseSchema, ItemResponseSchema, ItemsListRequestSchema, ItemsShowRequestSchema


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
        _sort = get(params, 'sort').lower() == 'asc' and 1 or -1
        res = ItemsHelper.get_items(_nft_id, _type, _page, _page_size, _sort)
        return res

class NFTShowResource(Resource):
    @security.http(
        params=ItemsShowRequestSchema(),
        response=ItemsListResponseSchema()
    )
    def get(self,params):
        _is_show = get(params , 'is_show')
        _page= get(params, 'page')
        _page_size = get(params, 'page_size')
        _sort = get(params, 'sort').lower() == 'asc' and 1 or -1
        res = ItemsHelper.get_items_show(_is_show , _page, _page_size, _sort)
        return res


