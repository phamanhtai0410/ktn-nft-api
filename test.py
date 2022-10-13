# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from bson import ObjectId
from eth_account.messages import encode_defunct
from web3 import Web3

from blockchain import Blockchain
from config import Config
from enums.order import Chains
from lib import dt_utcnow

items = [{"name": 1}]
for _item in items:
    _item['id'] = 1
print(items)

_w3 = Blockchain(
    Chains.BSC_CHAIN,
    Web3.HTTPProvider(Config.BSC_RPC_URI, request_kwargs={'timeout': 60}))

base_message = Web3.solidityKeccak(
    ['string', 'string', 'string[]', 'uint256'],
    ["abc", "abd", ["ae", "abdcq", "adteew"], int(dt_utcnow().timestamp())]
)
message = encode_defunct(base_message)
_signed_message = _w3.eth.account.sign_message(
    message,
    private_key=Config.AUTH_PRIVATE_KEY
)

print(message)
print(_signed_message.messageHash.hex())
print(_signed_message.signature.hex())

# _result = _w3.eth.account.recover_message(message, signature=_signed_message.signature)
#
# print(_result)
