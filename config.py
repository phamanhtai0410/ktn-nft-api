# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = False
    PROJECT = "nft-api"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')
    # Authentication
    AUTH_ADDRESS = os.getenv('AUTH_ADDRESS', '')

    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    # Config celery worker

    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.task_on_payment': {'queue': 'nft-payment-queue'},
        'worker.task_record_tx': {'queue': 'nft-payment-queue'},
        'worker.task_confirm_tx': {'queue': 'nft-confirm-tx-queue'}
    }
    PUBLIC_PATH = os.getenv('PUBLIC_PATH')
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER'))
    ADDRESS_OF_COUNTER = os.getenv('ADDRESS_OF_COUNTER')
    REDLOCK_REDIS =  json.loads(os.getenv('REDLOCK_REDIS','[]'))
    BSC_RPC_URI = os.getenv('BSC_RPC_URI')
    ETH_RPC_URI = os.getenv('ETH_RPC_URI')
    ASSETS = json.loads(os.getenv('ASSETS', '{}'))
