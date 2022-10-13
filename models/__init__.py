# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
__models__ = ['OrderModel']

from config import Config
from connect import connect_db, redis_cluster
from lib import DaoModel
from models.order import OrderDao

NFTDetailModel = DaoModel(col=connect_db.db.nft_details, redis=redis_cluster)
PromotionCodeModel = DaoModel(col=connect_db.db.promotion_codes, redis=redis_cluster)

PaymentConfigModel = DaoModel(col=connect_db.db.counters, redis=redis_cluster)

OrderModel = OrderDao(col=connect_db.db.orders, redis=redis_cluster, project=Config.PROJECT, broker=Config.BROKER_URL)
