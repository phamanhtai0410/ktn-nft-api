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
from lib.logger import debug
from schemas.iapi.order import ResultOrderSchema


class IAPIOrderResource(Resource):
    @security.http(
        form_data=ResultOrderSchema()
    )
    def put(self, form_data):
        debug(f'{form_data}')
        OrderHelper.on_minted(
            address=get(form_data, 'address'),
            order_id=get(form_data, 'order_id'),
            tx_hash=get(form_data, 'tx_hash'),
            token_ids=get(form_data, 'token_ids')
        )
        return {

        }
