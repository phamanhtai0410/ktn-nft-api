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
from schemas.items import CollectionRequestParams, CollectionResponseSchema


class CollectionResource(Resource):

    @security.http(
        params = CollectionRequestParams(),
        response=CollectionResponseSchema()
    )
    def get(self,params):
        _rarity = get(params, 'rarity')            
        res = ItemsHelper.get_items_with_rarity(_rarity)
        return res



        