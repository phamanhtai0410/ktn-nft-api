# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from pydash import get

from connect import security
from helper.order import OrderHelper
from schemas.order import OrderSchema, ResOrderSchema


class OrderResource(Resource):

    @security.http(
        form_data=OrderSchema(),
        response=ResOrderSchema()
    )
    def post(self, form_data):
        _result = OrderHelper.init(form_data)
        return _result

    @security.http(
        form_data=OrderSchema(),
        response=ResOrderSchema()
    )
    def put(self, form_data):
        return OrderHelper.make_payment(form_data)