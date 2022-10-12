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
from schemas.items import ItemRequestParams, ItemsListResponseSchema, ItemResponseSchema


class ItemsListResource(Resource):

    @security.http(
        response=ItemsListResponseSchema()
    )
    def get(self):          
        res = ItemsHelper.get_items()
        return res
    
class ItemResource(Resource):
    
    @security.http(
        params = ItemRequestParams(),
        response=ItemResponseSchema()
    )
    def get(self,params):
        _id = get(params,'_id')
        res = ItemsHelper.get_items_with_id(_id)
        return res


        