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
        _w3 = get(web3_providers, Chains.BSC_CHAIN)
        _base_message = Web3.solidityKeccak(
            ['uint256', 'uint256', 'string[]', 'string', 'uint256'],       # [chain_id, discount, cids, items, deadline]
            [get(data, 'chain_id'), get(data, 'discount'), get(data, 'cids'), get(data, 'items'), get(data, 'deadline')]
            # testnet chain_id=97, mainnet chain_id=56
        )
        message = encode_defunct(_base_message)
        _signed_message = _w3.eth.account.sign_message(
            message,
            private_key=Config.AUTH_PRIVATE_KEY
        )

        return _signed_message.signature.hex()
