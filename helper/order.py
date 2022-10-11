# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import random
import traceback
import uuid

import sentry_sdk
from pydash import get

from config import Config
from connect import dlm
from enums.order import Status
from exception import TxRecorded, TxPayment
from lib import NotFound
from lib.logger import debug
from models import NFTDetailModel, PaymentConfigModel, OrderModel
from tasks.order import task_record_tx


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
    def init(cls, form_data):
        _order_id = str(uuid.uuid4())
        _cost = sum([cls.get_cost_of(_item) for _item in get(form_data, 'items')])
        _address_of_counter = get(random.choice([PaymentConfigModel.find(
            filter={
                'chain': get(form_data, "chain")
            })]), 'address')

        OrderModel.insert_one({
            'address': get(form_data, 'address'),
            'order_id': _order_id,
            'cost': _cost,
            'items': get(form_data, 'items'),
            'address_of_counter': _address_of_counter,
            'created_by': get(form_data, 'address'),
            'status': Status.WAITING_FOR_PAYMENT
        }, worker=True)

        return {
            'order_id': _order_id,
            'cost': _cost,
            'address_of_counter': _address_of_counter,
            'unit': get(form_data, 'uint'),
            'chain': get(form_data, 'chain')
        }

    @staticmethod
    def lock_tx(chain, tx_hash):
        try:
            _lock = dlm.lock(f'ktn:logs:tx_hash:{chain}:{tx_hash}', 60 * 20)
            if _lock:
                debug(f'[EVENT] \033[92m ✔✔✔ Process .................. {tx_hash} \033[0m')
                return True
            else:
                debug(f'[EVENT] \033[93m ⚠⚠⚠ ______ Lock fail ______ {tx_hash} \033[0m')
        except:
            traceback.print_exc()
            sentry_sdk.capture_exception()
        return False

    @classmethod
    def make_payment(cls, form_data):
        _tx_hash = get(form_data, 'tx_hash')
        _tx_hash = _tx_hash.lower()
        if not cls.lock_tx(get(form_data, 'chain'), get(form_data, 'tx_hash')):
            raise TxRecorded()
        _order = OrderModel.find_one({
            'order_id': get(form_data, 'order_id')
        }, cache=True)
        if not _order:
            raise NotFound(msg="Not found order.")
        if get(_order, 'status') != Status.WAITING_FOR_PAYMENT:
            raise TxPayment()
        task_record_tx.delay(
            tx_hash=_tx_hash,
            order_id=get(form_data, 'order_id'),
            worker=True
        )
        return {
            'tx_hash': _tx_hash,
            'order_id': _order,
            'status': Status.CHECKING
        }
