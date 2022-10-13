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
from schemas.items import ItemsRequestParams, ItemsListResponseSchema


class ItemsResource(Resource):

    @security.http(
        params = ItemsRequestParams(),
        response=ItemsListResponseSchema()
    )
    def get(self,params):
        _rarity = get(params, 'rarity') 
        _id = get(params,'_id')
        if _id:
            res = ItemsHelper.get_items_with_id(_id)
           
        elif _rarity:
            res = ItemsHelper.get_items_with_rarity(_rarity)
                    
        else:
            res = ItemsHelper.get_items()
        return res

