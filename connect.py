# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import asyncio

import motor
from flask_pymongo import PyMongo
import motor.motor_asyncio
from rediscluster import RedisCluster
from web3 import Web3

from blockchain import Blockchain
from config import Config
from redlock import Redlock

from enums.order import Chains


class InterfaceAsync:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(Config.MONGO_URI)
        self.client.get_io_loop = asyncio.get_event_loop
        self.db = self.client.core


connect_db = PyMongo()

redis_cluster = RedisCluster(
    startup_nodes=Config.REDIS_CLUSTER,
    decode_responses=True,
    skip_full_coverage_check=True
)

dlm = Redlock(Config.REDLOCK_REDIS, retry_count=2)

web3_providers = {
    Chains.BSC_CHAIN: Blockchain(Chains.BSC_CHAIN,
                                 Web3.HTTPProvider(Config.BSC_RPC_URI, request_kwargs={'timeout': 60})),
    Chains.ETHEREUM_CHAIN: Blockchain(Chains.ETHEREUM_CHAIN,
                                      Web3.HTTPProvider(Config.ETH_RPC_URI, request_kwargs={'timeout': 60}))
}

from lib import HTTPSecurity

security = HTTPSecurity(redis=redis_cluster, auth_address=Config.AUTH_ADDRESS)
