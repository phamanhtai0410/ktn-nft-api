# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from helper.box import BoxHelper
from schemas.box import BoxSchema


class AllsFilterResource(Resource):

    @security.http(
        
    )
    def get(self):
        return {
            'result': 'test'
        }

