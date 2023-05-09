from pydash import get
from web3 import Web3
from connect import redis_cluster
from config import Config
from exception import ExPromoCodeInvalid, ExRefCodeInvalid, ExRefCodeOwner
from exceptions.metadata import NotMintStartTimeYetEx, UserMintLimitAmountEx, UserNotInWhitelistEx
from lib import dt_utcnow
from lib.enum import NFT_AMOUNT_PUBLIC_MINT
from models import CollectionModel, NFTsModel, NftWhitelistModel, PromotionCodeModel, ReferralModel, PromotionCodeUsedLogModel
import pydash as py_

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
            # if get(_referral, 'address') == address:
            #     raise ExRefCodeOwner()

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
        """
        [
            chain_id,
            nonce, 
            user_address, 
            creator_contract_address,
            collection_address, 
            discount, 
            is_whitelist_mint,
            nftIndexes[],
            deadline
        ]
        """
        _encode = _w3.codec.encode_abi(
            [
                'uint256',
                'address',
                'address',
                'address',
                'uint256',
                'bool',
                'uint256[]',
                'uint256',
                'uint256'
            ],
            [
                get(data, 'chain_id'),
                get(data, 'address'),
                get(data, 'contract'),
                get(data, 'collection'),
                get(data, 'discount'),
                get(data, 'is_whitelist_mint'),
                get(data, 'nft_indexes'),
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

    @staticmethod
    def count_nft_minted(collection_address, address):
        _total_amount = NFTsModel.col.count_documents({
            'address': address,
            'contract': collection_address
        })

        print('total_mint', _total_amount)

        return _total_amount

    @staticmethod
    def check_whitelist(collection_address, address, mint_amount):
        _nft_whitelist = NftWhitelistModel.find_one({
            'collection': collection_address,
            'address': address
        }, cache=True)
        _nft_collection = CollectionModel.find_one({
            'address': collection_address
        }, cache=True)

        _whitelist_time = get(_nft_collection, 'whitelist_time', [])
        if not _whitelist_time:
            raise NotMintStartTimeYetEx

        _now = dt_utcnow()
        # NOTE: if have any time in range at now -> can mint
        _check_whitelist_time = py_.find(_whitelist_time, lambda x: py_.get(x, 'start_time') <= _now.timestamp() and py_.get(x, 'end_time') >= _now.timestamp())
        if not _check_whitelist_time:
            raise NotMintStartTimeYetEx

        if (not _nft_whitelist or not _nft_collection) and py_.get(_check_whitelist_time, 'is_public', False) == False:
            raise UserNotInWhitelistEx

        _total_amount = get(_nft_whitelist, 'amount', 0) if py_.get(_check_whitelist_time, 'is_public', False) == False or _nft_whitelist else NFT_AMOUNT_PUBLIC_MINT
        _minted_amount = MetaDataHelper.count_nft_minted(collection_address=collection_address, address=address)
        if _minted_amount + mint_amount > _total_amount:
            raise UserMintLimitAmountEx

        return {
            'minted_amount': _minted_amount,
            'is_in_whitelist': True if _nft_whitelist else False,
            'total_amount': _total_amount,
            'whitelist_time': _check_whitelist_time
        }


