# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
# from helper.sync import sync_task
import traceback

import requests
import sentry_sdk
from pydash import get
from web3 import Web3

from config import Config
from connect import web3_providers
# from enums.items import rarity_codes
from enums.order import Status
from helper.ipfs import IPFSHelper
from helper.socket import SocketEmitter
from lib import dt_utcnow
from lib.logger import debug
from worker import worker
import models as models

_web3 = Web3()


@worker.task(name='worker.task_generate_metadata_file', rate_limit='1000/s')
def task_generate_metadata_file(order_id):
    try:
        _order = models.OrderModel.find_one({
            'order_id': order_id
        })
        if get(_order, 'status') != Status.CONFIRMED:
            sentry_sdk.capture_message(
                f"Waining: Status of order#{order_id} is {get(_order, 'status')}. Required: status={Status.CONFIRMING}")
        models.OrderModel.update_one({
            'order_id': order_id
        }, obj={
            'updated_by': 'task_generate_metadata_file',
            'status': Status.MINING
        })
        SocketEmitter.emit(
            room_id=get(_order, 'address'),
            event="ORDER_STEP",
            value={
                'order_id': order_id,
                'tx_hash': get(_order, 'tx_hash'),
                'status': Status.MINING
            }
        )

        _items = get(_order, 'items')
        for _item in _items:
            _meta = {
                "description": get(_item, 'description'),
                "external_url": "",
                "image": get(_item, 'image'),
                "name": get(_item, 'name'),
                "attributes": [
                    {
                        "display_type": "number",
                        "trait_type": "rarity",
                        "value": get(_item, 'rarity')
                    },
                    {
                        "display_type": "number",
                        "trait_type": "type",
                        "value": get(_item, 'type')
                    }
                ]
            }
            _cid = IPFSHelper.upload_web3(_meta)
            _item['cid'] = _cid
        res = requests.post(f'{Config.WALLET_IAPI}/mint', json={
            'address': get(_order, 'address'),
            'items': [{
                'rarity': get(_item, 'rarity'),
                'cid': get(_item, 'cid'),
                'type': get(_item, 'type')
            } for _item in _items],
            'order_id': order_id,
            'contract_address': Config.NFT_ADDRESS
        })
        debug(f"Response from wallet: {res.text}")
        _task_id = ""
        if res.status_code == 200:
            _task_id = get(res.json(), 'data.task_id')
        else:
            sentry_sdk.capture_message(
                f"Waining: Send request mint for order#{order_id} with error: {res.text}. Please re-check.")
        models.OrderModel.update_one({
            'order_id': order_id
        }, obj={
            'updated_by': 'task_generate_metadata_file',
            'task_id': _task_id,
            'cid_items': _items
        })

        return f"Done: Generate metadata file for order#{order_id}"
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return f"Failed: Generate metadata file for order#{order_id}"


@worker.task(name='worker.task_on_payment', rate_limit='1000/s', default_retry_delay=3,
             retry_kwargs={'max_retries': 1, 'countdown': 3})
def task_on_payment(order_id):
    try:
        _order = models.OrderModel.find_one({
            'order_id': order_id
        })
        if get(_order, 'status') != Status.CHECKING:
            sentry_sdk.capture_message(
                f"The order #{order_id} has been checked. Please re-check it.")
            return "Failed"
        debug(f'web3_providers {web3_providers}')
        debug(get(_order, 'chain'))
        _w3 = get(web3_providers, get(_order, 'chain'))
        _tx_info, _tx = _w3.get_transfer_info(
            token=get(_order, 'unit'),
            tx_hash=get(_order, 'tx_hash')
        )
        if _tx_info == -1 and dt_utcnow().timestamp() - get(_order, 'payment_time').timestamp() < 60 * 2:
            task_on_payment.retry()
            return f"Retry: order_id {order_id}"
        else:
            # set target block
            _target_block = get(_tx, 'blockNumber', 0) + 10 if get(_tx, 'blockNumber') else 0
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
                if get(_update, 'status') == Status.FAILED:
                    return SocketEmitter.emit(
                        room_id=get(_order, 'address'),
                        event="ORDER_FAIL",
                        value={
                            'order_id': order_id,
                            'tx_hash': get(_order, 'tx_hash'),
                            'msg': get(_update, 'reason')
                        }
                    )
                return f"Executed successfully {order_id}"

            if not _tx_info or isinstance(_tx_info, str):
                _update['status'] = Status.FAILED
                _update['reason'] = _tx_info
                return completed()

            if get(_tx, 'status') != 1:
                _update['status'] = Status.FAILED
                _update['reason'] = 'Tx has failed.'
                return completed()

            _from = get(_tx_info, 'args.from')
            _amount = get(_tx_info, 'args.value')
            _to = get(_tx_info, 'args.to')
            debug(f'info {_from} {_to} {_amount} {get(_order, "address_of_counter")}')
            if _to.lower() != get(_order, 'address_of_counter').lower():
                _update['status'] = Status.FAILED
                _update['reason'] = 'Address of counter invalid.'

                return completed()

            debug(f"dec {_w3.decimals} {get(_order, 'unit')}")
            _order_amount = _w3.to_wei(
                amount=get(_order, 'cost'),
                decimal=_w3.decimals[get(_order, 'unit')]
            )
            # Check amount
            debug(f'Amount {_order_amount} {_amount}')
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
            _update['status'] = Status.CONFIRMING
            completed()
            task_confirm_tx.delay(
                order_id=order_id,
                tx_hash=get(_order, 'tx_hash'),
                chain=get(_order, 'chain'),
                target_block=_target_block,
                address=get(_order, 'address')
            )
            SocketEmitter.emit(
                room_id=get(_order, 'address'),
                event="ORDER_STEP",
                value={
                    'order_id': order_id,
                    'tx_hash': get(_order, 'tx_hash'),
                    'status': Status.CONFIRMING,
                    'target_block': _target_block
                }
            )
            return f"Next process: {order_id}  at block {_target_block}"
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return f"Fail: {order_id}"


@worker.task(name='worker.task_confirm_tx', rate_limit='1000/s', default_retry_delay=10)
# @sync_task
def task_confirm_tx(order_id, tx_hash, chain, target_block, address):
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
                    if get(_order, 'status') != Status.CONFIRMING:
                        sentry_sdk.capture_message(
                            f"Warning:  Status of order#{order_id} is not {Status.CONFIRMING}. It is {get(_order, 'status')}")

                        return f"Fail: Status of order#{order_id} is not {Status.CONFIRMING}. It is {get(_order, 'status')}"

                    models.OrderModel.update_one(filter={
                        'order_id': order_id
                    }, obj={
                        'status': Status.CONFIRMED,
                        'verify_at': _current_block,
                        'updated_by': 'task_confirm_tx'
                    })
                    # TODO call mint nft
                    task_generate_metadata_file.delay(
                        order_id=order_id
                    )
                    SocketEmitter.emit(
                        room_id=address,
                        event="ORDER_STEP",
                        value={
                            'order_id': order_id,
                            'tx_hash': tx_hash,
                            'status': Status.CONFIRMED
                        }
                    )
                    return f"Done: Confirm tx#{tx_hash} of order#{order_id}"
            except:
                sentry_sdk.capture_exception()
                traceback.print_exc()

            models.OrderModel.update_one(filter={
                'order_id': order_id
            }, obj={
                'status': Status.FAILED,
                'reason': 'tx validation failed.',
                'updated_by': 'task_confirm_tx'
            })
            SocketEmitter.emit(
                room_id=address,
                event="ORDER_FAIL",
                value={
                    'order_id': order_id,
                    'tx_hash': tx_hash,
                    'status': Status.FAILED,
                    'msg': 'tx validation failed.'
                }
            )
            return f"Confirm: {order_id} "

        else:
            task_confirm_tx.retry()
            return f"Retry confirm {order_id}"
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return f"Fail confirm: {order_id}"


@worker.task(name='worker.task_record_tx', rate_limit='1000/s', default_retry_delay=10)
def task_record_tx(tx_hash, order_id):
    _order = models.OrderModel.find_one({
        'order_id': order_id
    })
    # if get(_order, 'status') != Status.INIT:
    #     return f"Fail: status of order#{order_id} is not {Status.INIT}"
    _tx_hash = models.OrderModel.find_one({
        'tx_hash': tx_hash
    })
    if _tx_hash:
        sentry_sdk.capture_message(
            f"Tx#{tx_hash} was logged but it was sent back. Please double check order #{order_id}")
        return SocketEmitter.emit(
            room_id=get(_order, 'address'),
            event="ORDER_FAIL",
            value={
                'order_id': order_id,
                'tx_hash': tx_hash,
                'msg': 'The transaction hash has been used.'
            }
        )

    if not _order:
        sentry_sdk.capture_message(f"Not found order_id #{order_id}. Please re-check tx #{tx_hash}")
        return SocketEmitter.emit(
            room_id=get(_order, 'address'),
            event="ORDER_FAIL",
            value={
                'order_id': order_id,
                'tx_hash': tx_hash,
                'msg': 'Not found order.'
            }
        )
    if get(_order, 'status') != Status.WAITING_FOR_PAYMENT:
        sentry_sdk.capture_message(
            f"The order #{order_id} has been out of payment status. Please re-check tx #{tx_hash}")
        return SocketEmitter.emit(
            room_id=get(_order, 'address'),
            event="ORDER_FAIL",
            value={
                'order_id': order_id,
                'tx_hash': _tx_hash,
                'msg': 'The order was not found in the payment queue.'
            }
        )
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

    return SocketEmitter.emit(
        room_id=get(_order, 'address'),
        event="ORDER_STEP",
        value={
            'order_id': order_id,
            'tx_hash': _tx_hash,
            'status': Status.CHECKING
        }
    )
