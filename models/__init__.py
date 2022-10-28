# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
__models__ = ['OrderModel', 'PromotionCodeModel']

from config import Config
from connect import connect_db, redis_cluster
from lib import DaoModel
from models.order import OrderDao

NFTDetailModel = DaoModel(col=connect_db.db.nft_details, redis=redis_cluster)

PromotionCodeModel = DaoModel(col=connect_db.db.promotion_codes, redis=redis_cluster, project=Config.PROJECT,
                              broker=Config.BROKER_URL)
ReferralModel = DaoModel(col=connect_db.db.referral, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

PaymentConfigModel = DaoModel(col=connect_db.db.counters, redis=redis_cluster)

OrderModel = OrderDao(col=connect_db.db.orders, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)

NFTsModel = DaoModel(col=connect_db.db.nfts, redis=redis_cluster)

CollectionModel = DaoModel(col=connect_db.db.collection, redis=redis_cluster)

NFTsHistoryModel = DaoModel(col=connect_db.db.nfts_history, redis=redis_cluster)

ReferralModel = DaoModel(connect_db.db.referral, redis=redis_cluster)
