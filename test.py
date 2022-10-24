# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from eth_account.messages import encode_defunct
from eth_utils import to_bytes
from web3 import Web3

_web3 = Web3()
privateKey = '98102796d0dfe116f5af6e9a3c10dc38d316f6c98b3ded8d008b962c7d126460'
_encode = _web3.codec.encode_abi([
        "uint256",
        "address",
        "address",
        "uint256",
        "string[]",
        "uint8[]",
        "uint8[]",
        "uint256"
    ],
    [
        97,
        "0x183Ff214179cd2B1c06A937D663F192340edd159",
        "0x3E9DFe8715d4034AF6F3A070F0C07Ff2B1bc2fCB",
        0,
        [
            "bafkreidfudijruu7e4mjgehgr3szr3rexyqlno3wafg3qqgtmbyj6i7d3y",
            "bafkreie2bsk3u4kgxtnlqpf652eil37fkhqs5zx5laozag7jsq76rualf4",
            "bafkreicqngcb44wqklgxjozrhw4ge67bjxlrmi7hkyyedkkfrynnil34zu",
            "bafkreifiuytiisforeksrt3aw3itv3ajc6wsxm6pvknawoj3nk5t2tm64e"
        ],
        [1, 2, 3, 5],
        [2, 2, 2, 2],
        1666341253
    ])

digest = _web3.solidityKeccak(['bytes'], [f'0x{_encode.hex()}'])
_signed_message = _web3.eth.account.signHash(
    digest,
    private_key=privateKey
)
print({
    'signature': _signed_message.signature.hex()
})
