from eth_account.messages import encode_defunct
from pydash import get
from web3 import Web3

from config import Config
from connect import web3_providers
from enums.order import Chains
from exception import ExPromoCodeInvalid
from lib import dt_utcnow
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
        return get(_promotion, 'discount', 0)

    @staticmethod
    def update_used_promotion_code(promotion_code):
        PromotionCodeModel.update_one(
            filter={'code': promotion_code},
            obj={
                'updated_by': 'metadata:update_used_promotion_code',
                'status': False
            }
        )

    @staticmethod
    def generate_signature(data):
        print(data)
        _w3 = get(web3_providers, Chains.BSC_CHAIN)
        _base_message = Web3.solidityKeccak(
            [
                'uint256',
                'address',
                'address',
                'uint256',
                'bytes32[]',
                'uint8[]',
                'uint8[]',
                'uint256'
            ],  # [chain_id, user_address, contract_address, discount, cids, types, rarities, deadline]
            [
                _w3.eth.chain_id,
                get(data, 'address'),
                get(data, 'contract'),
                get(data, 'discount'),
                get(data, 'cids_bytes'),
                get(data, 'types'),
                get(data, 'rarities'),
                get(data, 'deadline')
            ]
        )
        message = encode_defunct(_base_message)
        _signed_message = _w3.eth.account.sign_message(
            message,
            private_key=Config.AUTH_PRIVATE_KEY
        )

        return _signed_message.signature.hex()
