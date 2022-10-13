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
        _id = get(params, '_id')    
        if not _id:
            res = ItemsHelper.get_collections_list()
        else:
            res = ItemsHelper.get_collection(_id)
        return res



        