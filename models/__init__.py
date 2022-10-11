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
from models.items import ItemsDao
import models.order as as_order

NFTDetailModel = DaoModel(col=connect_db.db.nft_details, redis=redis_cluster)

PaymentConfigModel = DaoModel(col=connect_db.db.payment_config, redis=redis_cluster)

OrderModel = as_order.OrderDao(col=connect_db.db.orders, redis=redis_cluster, broker=Config.BROKER_URL, project=Config.PROJECT)

ItemsModel = ItemsDao(col=connect_db.db.nft_details, redis=redis_cluster)