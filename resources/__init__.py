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

api_resources = {
    '/hello': HelloWorld,
    '/common/health_check': HealthCheck,
    **{f'/iapi{k}': val for k, val in iapi_resources.items()},
    '/order': OrderResource,
    '/items': ItemsListResource,
    '/collections': CollectionResource,
    '/my_nfts': MyNFTsResource,
    '/metadata': MetaDataResource,
    '/nfts_history': NFTsHistoryResource,
    '/nfts_show': NFTShowResource,
    '/promo_code': PromoResource,
    '/referral_code': ReferralResource,
    '/box': BoxResource
}
