from pydash import get
from web3 import Web3
from config import Config


class ForgingHelpers:

    @staticmethod
    def generate_signature(data):
        _w3 = Web3()
        """
        [
            chain_id, 
            user_address, 
            forging_address,
            collection_address, 
            collection_addresses_forging, 
            token_ids_forging,
            nft_indexes_forging,
            nonce,
            deadline
        ]
        """
        _encode = _w3.codec.encode_abi(
            [
                'uint256',
                'address',
                'address',
                'address',
                'address[]',
                'uint256[]',
                'uint256[]',
                'uint256',
                'uint256'
            ],
            [
                get(data, 'chain_id'),
                get(data, 'user_address'),
                get(data, 'forging_address'),
                get(data, 'collection_address'),
                get(data, 'collection_addresses_forging'),
                get(data, 'token_ids_forging'),
                get(data, 'nft_indexes_forging'),
                get(data, 'nonce'),
                get(data, 'deadline')
            ]
        )
        digest = Web3.solidityKeccak(['bytes'], [f'0x{_encode.hex()}'])
        _signed_message = _w3.eth.account.signHash(
            digest,
            private_key=Config.AUTH_PRIVATE_KEY
        )

        return _signed_message.signature.hex()
