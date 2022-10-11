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
from schemas.items import ItemsRequestParams, ItemsResponseSchema, ItemsListResponseSchema


class ItemsResource(Resource):

    @security.http(
        params = ItemsRequestParams(),
        response=ItemsListResponseSchema()
    )
    def get(self,params):
        _rarity_code = get(params, 'rarity_code') 
        if not _rarity_code:
            res = ItemsHelper.get_items()
        else:
            res = ItemsHelper.get_items_with_rarity(_rarity_code)
        return res
        