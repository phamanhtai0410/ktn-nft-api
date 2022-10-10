# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
__models__ = []

from connect import connect_db, redis_cluster
from lib import DaoModel
from models.order import OrderDao

NFTDetailModel = DaoModel(col=connect_db.db.nft_details, redis=redis_cluster)

PaymentConfigModel = DaoModel(col=connect_db.db.payment_config, redis=redis_cluster)

OrderModel = OrderDao(col=connect_db.db.orders, redis=redis_cluster)
