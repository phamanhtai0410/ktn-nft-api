# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security


class FiatResource(Resource):


    @security.http()
    def get(self, params):
        pass

