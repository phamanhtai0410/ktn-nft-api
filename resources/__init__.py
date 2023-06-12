# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.box import BoxResource
from resources.health_check import HealthCheck
from resources.hello import HelloWorld
from resources.iapi import iapi_resources
from resources.items import ItemsListResource
from resources.items import NFTShowResource
from resources.metadata import MetaDataResource
from resources.order import OrderResource
from resources.items import ItemsListResource
from resources.collection import CollectionResource
from resources.my_nfts import MyNFTsResource
from resources.nfts_history import NFTsHistoryResource
from resources.promotion import PromoResource
from resources.referral import ReferralResource
from resources.box import BoxResource
from resources.signature_box import SignatureBoxResource
from resources.forging_result import ForgingResultResource
from resources.forging_list import ForgingListResource
from resources.forging_signature import ForgingSignatureResource

api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    '/order': OrderResource,
    '/items': ItemsListResource,
    '/collections': CollectionResource,
    '/my_nfts': MyNFTsResource,
    '/metadata': MetaDataResource,
    '/signature_box': SignatureBoxResource,
    '/nfts_history': NFTsHistoryResource,
    '/nfts_show': NFTShowResource,
    '/promo_code': PromoResource,
    '/referral_code': ReferralResource,
    '/box': BoxResource,
    '/forging/result': ForgingResultResource,
    '/forging/available_list': ForgingListResource,
    '/forging/signature': ForgingSignatureResource,
}
