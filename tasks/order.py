# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
# from helper.sync import sync_task
import traceback

import sentry_sdk
from pydash import get
from web3 import Web3

from connect import web3_providers
from enums.order import Status
from lib import dt_utcnow
from worker import worker
import models as models

_web3 = Web3()


@worker.task(name='worker.task_on_payment', rate_limit='1000/s', default_retry_delay=10)
def task_on_payment(order_id):
    try:
        _order = models.OrderModel.find_one({
            'order_id': order_id
        })
        if get(_order, 'status') != Status.CHECKING:
            sentry_sdk.capture_message(
                f"The order #{order_id} has been checked. Please re-check it.")
            return "Failed"
        _w3 = get(web3_providers, get(_order, 'chain'))
        _tx_info, _tx = _w3.get_transfer_info(
            token=get(_order, 'unit'),
            tx_hash=get(_order, 'tx_hash')
        )
        if _tx_info == -1 and dt_utcnow().timestamp() - get(_order, 'payment_time').timestamp() < 60 * 3:
            task_on_payment.retry()
            return f"Retry: order_id {order_id}"
        else:
            # set target block
            _target_block = get(_tx, 'blockNumber', 0) + 10 if _tx else 0
            _update = {
                'updated_by': 'worker_checking',
                'event': _tx_info,
                'tx_info': _tx,
                'confirm_block': _target_block
            }

            def completed():
                models.OrderModel.update_one(filter={
                    'order_id': order_id
                }, obj=_update)
                return f"Executed successfully {order_id}"

            if not _tx_info or isinstance(_tx_info, str):
                _update['status'] = Status.FAILED
                _update['reason'] = _tx_info
                return completed()

            if get(_tx_info, 'status') != 1:
                _update['status'] = Status.FAILED
                _update['reason'] = 'Tx has failed.'
                return completed()

            _from = get(_tx_info, 'form')
            _amount = get(_tx_info, 'amount')
            _to = get(_tx_info, 'to')

            if _to.lower() != get(_order, 'address_of_counter').lower():
                _update['status'] = Status.FAILED
                _update['reason'] = 'Address of counter invalid.'

                return completed()

            if _to.lower() != get(_order, 'address_of_counter').lower():
                _update['status'] = Status.FAILED
                _update['reason'] = 'Address of counter invalid.'

                return completed()
            _order_amount = _w3.to_wei(
                amount=get(_order, 'cost'),
                decimal=_w3.decimals[get(_order, 'uint')]
            )
            # Check amount
            if _order_amount != _amount:
                _update['status'] = Status.FAILED
                _update['reason'] = 'Amount invalid.'
                return completed()
            # Check user
            if _from.lower() != get(_order, 'address'):
                _update['status'] = Status.FAILED
                _update['reason'] = 'address of tx invalid.'
                return completed()

            _update['waiting_for_confirm'] = True
            _update['status'] = Status.CONFIRM
            completed()
            if _target_block:
                task_confirm_tx.delay(
                    order_id=order_id,
                    tx_hash=get(_order, 'tx_hash'),
                    chain=get(_order, 'chain'),
                    target_block=_target_block
                )
            return f"Next process: {order_id}  at block {_target_block}"
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return f"Fail: {order_id}"


@worker.task(name='worker.task_confirm_tx', rate_limit='1000/s', default_retry_delay=10)
# @sync_task
def task_confirm_tx(order_id, tx_hash, chain, target_block):
    try:
        _w3 = get(web3_providers, chain)
        _current_block = _w3.eth.get_block_number()
        print('_block', _current_block, target_block)
        if _current_block >= target_block:

            try:
                _tx_info = _w3.eth.get_transaction_receipt(
                    tx_hash
                )
                if get(_tx_info, 'status') == 1:
                    _order = models.OrderModel.find_one({
                        'order_id': order_id
                    })
                    # Check status
                    if get(_order, 'status') != Status.CONFIRM:
                        sentry_sdk.capture_message(f"Warning:  {order_id}")
                        return f"Fail: Status of order#{order_id} is not {Status.CONFIRM}. It is {get(_order, 'status')}"

                    models.OrderModel.update_one(filter={
                        'order_id': order_id
                    }, obj={
                        'status': Status.MINING,
                        'verify_at': _current_block
                    })
                    # TODO call mint nft
            except:
                sentry_sdk.capture_exception()

            models.OrderModel.update_one(filter={
                'order_id': order_id
            }, obj={
                'status': Status.FAILED,
                'reason': 'Confirm tx has fie'
            })
            return f"Confirm: {order_id} "

        else:
            task_confirm_tx.retry()
            return f"Retry confirm {order_id}"
    except:
        sentry_sdk.capture_exception()
        return f"Fail confirm: {order_id}"


@worker.task(name='worker.task_record_tx', rate_limit='1000/s', default_retry_delay=10)
def task_record_tx(self, tx_hash, order_id):
    _order = self.find_one({
        'order_id': order_id
    })
    # if get(_order, 'status') != Status.INIT:
    #     return f"Fail: status of order#{order_id} is not {Status.INIT}"
    _tx_hash = self.find_one({
        'tx_hash': tx_hash
    })
    if _tx_hash:
        sentry_sdk.capture_message(
            f"Tx#{tx_hash} was logged but it was sent back. Please double check order #{order_id}")

    if not _order:
        sentry_sdk.capture_message(f"Not found order_id #{order_id}. Please re-check tx #{tx_hash}")
        return "Failed"

    if get(_order, 'status') != Status.WAITING_FOR_PAYMENT:
        sentry_sdk.capture_message(
            f"The order #{order_id} has been out of payment status. Please re-check tx #{tx_hash}")
        return "Failed"
    # Record status of order
    models.OrderModel.update_one({
        'order_id': order_id
    }, obj={
        'updated_by': 'worker',
        'status': Status.CHECKING,
        'tx_hash': tx_hash,
        'payment_time': dt_utcnow()
    })

    task_on_payment.delay(
        order_id=order_id
    )

    return "Done"
