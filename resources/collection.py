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
from schemas.items import CollectionRequestParams, CollectionListResponseSchema


class CollectionResource(Resource):

    @security.http(
        params = CollectionRequestParams(),
        response=CollectionListResponseSchema()
    )
    def get(self,params):
        _id = get(params, 'collection_id')          
        _page= get(params, 'page')
        _page_size = get(params, 'page_size')  
        if _id is None:
            res = ItemsHelper.get_collections_list(_page, _page_size)
            
        else:
            res = ItemsHelper.get_collection(_id, _page, _page_size)
        return res



        