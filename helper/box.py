# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get
from web3 import Web3

from config import Config
from models import BoxModel


class BoxHelper:

    @staticmethod
    def active():
        return BoxModel.find_one({
            'active': True
        })

    @staticmethod
    def by_id(box_id):
        return BoxModel.find_one({
            'box_id': box_id
        })

    @staticmethod
    def generate_signature(data):
        _w3 = Web3()
        _encode = _w3.codec.encode_abi(
            [
                'uint256',
                'address',
                'address',
                'address',
                'uint256',
                'uint256',
                'uint256'
            ],  # [chain_id, user_address, contract_address, collection_address, discount, amount, deadline]
            [
                Config.CHAIN_ID,
                get(data, 'address'),
                get(data, 'contract'),
                get(data, 'collection'),
                get(data, 'discount'),
                get(data, 'amount'),
                get(data, 'deadline')
            ]

        )
        digest = Web3.solidityKeccak(['bytes'], [f'0x{_encode.hex()}'])
        _signed_message = _w3.eth.account.signHash(
            digest,
            private_key=Config.AUTH_PRIVATE_KEY
        )

        return _signed_message.signature.hex()
