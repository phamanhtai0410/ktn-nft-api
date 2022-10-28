from pydash import get
from web3 import Web3

from config import Config
from exception import ExPromoCodeInvalid
from models import PromotionCodeModel


class MetaDataHelper:
    @staticmethod
    def discount(promotion_code):
        if promotion_code is None:
            return 0

        _promotion = PromotionCodeModel.find_one({
                'code': promotion_code
            })

        if not get(_promotion, 'status'):
            raise ExPromoCodeInvalid()
        return int(get(_promotion, 'discount', 0))

    @staticmethod
    def update_used_promotion_code(promotion_code, address):
        PromotionCodeModel.update_one(
            filter={'code': promotion_code},
            obj={
                'updated_by': 'metadata:update_used_promotion_code',
                'status': False,
                'address': address
            },
            worker=True
        )

    @staticmethod
    def generate_signature(data):
        _w3 = Web3()
        _encode = _w3.codec.encode_abi(
            [
                'uint256',
                'address',
                'address',
                'uint256',
                'string[]',
                'uint8[]',
                'uint8[]',
                'uint256'
            ],  # [chain_id, user_address, contract_address, discount, cids, types, rarities, deadline]
            [
                Config.CHAIN_ID,
                get(data, 'address'),
                get(data, 'contract'),
                get(data, 'discount'),
                get(data, 'cids'),
                get(data, 'types'),
                get(data, 'rarities'),
                get(data, 'deadline')
            ]
        )
        digest = Web3.solidityKeccak(['bytes'], [f'0x{_encode.hex()}'])
        _signed_message = _w3.eth.account.signHash(
            digest,
            private_key=Config.AUTH_PRIVATE_KEY
        )

        return _signed_message.signature.hex()
