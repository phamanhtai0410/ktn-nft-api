from pydash import get
from web3 import Web3
from connect import redis_cluster
from config import Config
from exception import ExPromoCodeInvalid, ExRefCodeInvalid, ExRefCodeOwner
from models import PromotionCodeModel, ReferralModel


class MetaDataHelper:
    @staticmethod
    def promotion_discount_percent(promotion_code):
        if promotion_code is None:
            return 0

        _promotion = PromotionCodeModel.find_one({
            'code': promotion_code
        })

        if get(_promotion, 'used') >= get(_promotion, 'total'):
            raise ExPromoCodeInvalid()
        if not get(_promotion, 'status'):
            raise ExPromoCodeInvalid()

        _promotion_code_used = redis_cluster.get(f'katana-dapp.promotion_code_used/{promotion_code}')

        if int(_promotion_code_used) >= get(_promotion, 'total'):
            raise ExPromoCodeInvalid()

        return get(_promotion, 'discount', 0)


    @staticmethod
    def referral_discount_percent(ref_code, address):
        if ref_code is not None:
            _referral = ReferralModel.find_one({
                'code': ref_code
            })

            if _referral is None:
                raise ExRefCodeInvalid()
            if get(_referral, 'address') == address:
                raise ExRefCodeOwner()

            return ref_code

        _referral = ReferralModel.find_one({
            'address': address
        })

        return get(_referral, 'code_linked', '')

    @staticmethod
    def update_used_promotion_code(promotion_code, address):
        _key = f'katana-dapp.promotion_code_used/{promotion_code}'
        redis_cluster.incr(name=_key, amount=1)

        PromotionCodeModel.update_one(
            filter={'code': promotion_code},
            extract={
                '$inc': {
                    'used': 1
                }
            },
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
