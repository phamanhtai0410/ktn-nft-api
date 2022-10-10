# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from schemas.order import OrderSchema, ResOrderSchema


class OrderResource(Resource):

    @security.http(
        form_data=OrderSchema(),
        response=ResOrderSchema()
    )
    def post(self, form_data):
        _items = get(form_data, 'items')
        _address = get(form_data, 'address')

    @security()
    def put(self, form_data):
        _items = get(form_data, 'items')
        _address = get(form_data, 'address')
