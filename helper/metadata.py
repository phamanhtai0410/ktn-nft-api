from pydash import get
from web3 import Web3
from connect import redis_cluster
from config import Config
from exception import ExPromoCodeInvalid, ExRefCodeInvalid, ExRefCodeOwner
from lib import dt_utcnow
from models import PromotionCodeModel, ReferralModel, PromotionCodeUsedLogModel


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

        _key = f'katana-dapp.promotion_code_used/{promotion_code}'
        _promotion_code_used = redis_cluster.incr(name=_key, amount=1)

        if int(_promotion_code_used) > get(_promotion, 'total'):
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
    def check_ref_code(ref_code):

        _referral = ReferralModel.find_one({
            'code': ref_code
        })

        if _referral is None:
            raise ExRefCodeInvalid()

        return True

    @staticmethod
    def update_used_promotion_code(promotion_code, address, order_id=None, updated_by=''):
        _obj = {
            'address': address,
            'code': promotion_code,
            'created_by': updated_by,
            'created_time': dt_utcnow()
        }

        if order_id is not None:
            _obj['order_id'] = order_id

        PromotionCodeModel.update_one(
            filter={'code': promotion_code},
            extract={
                '$inc': {
                    'used': 1
                }
            },
            obj={
                'updated_by': updated_by
            },
            worker=True
        )

        PromotionCodeUsedLogModel.insert_one(
            row=_obj,
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
                'address',
                'uint256',
                'string[]',
                'uint8[]',
                'uint256'
            ],  # [chain_id, user_address, contract_address, collection, discount, cids, rarities, deadline]
            [
                Config.CHAIN_ID,
                get(data, 'address'),
                get(data, 'contract'),
                get(data, 'collection'),
                get(data, 'discount'),
                get(data, 'cids'),
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
