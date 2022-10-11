# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from blockchain.abi import erc20_abi
from connect import web3_providers





class ChainHelper:

    @staticmethod
    def _web3(chain):

        return get(web3_providers, chain)

    @staticmethod
    def _erc20(address, web3):
        return web3.eth.contract(
            address,
            abi=erc20_abi
        )

    @classmethod
    def get_tx_detail(cls, tx_hash, chain):

        return
