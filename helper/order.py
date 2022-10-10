# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import random
import uuid

from pydash import get

from config import Config
from lib import NotFound
from models import NFTDetailModel, PaymentConfigModel


class OrderHelper:
    @staticmethod
    def get_cost_of(item):
        _info = NFTDetailModel.find_one({
            "_id": get(item, '_id')
        })

        if not _info:
            raise NotFound(msg='Not found item.')

        return float(get(_info, 'price') * get(item, 'amount'))

    @classmethod
    def make(cls, form_data):
        _order_id = str(uuid.uuid4())
        _cost = sum([cls.get_cost_of(_item) for _item in get(form_data, 'items')])
        _address_of_counter = get(random.choice([PaymentConfigModel.find(
            filter={
                'chain': get(form_data, "chain")
            })]), 'address')
        return {
            'order_id': _order_id,
            'cost': _cost,
            'address_of_counter': _address_of_counter,
            'unit': get(form_data, 'uint'),
            'chain': get(form_data, 'chain')
        }
