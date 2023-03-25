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
    DEBUG = os.getenv("DEBUG")
    PROJECT = "nft-api"
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    # Setup db
    MONGO_URI = os.getenv('MONGO_URI')
    # Authentication
    AUTH_ADDRESS = os.getenv('AUTH_ADDRESS', '')
    AUTH_PRIVATE_KEY = os.getenv('AUTH_PRIVATE_KEY', '')

    CELERY_IMPORTS = ['tasks']
    ENABLE_UTC = True

    # Config celery worker

    BROKER_URL = os.getenv('BROKER_URL')
    CELERY_QUEUES = os.getenv('CELERY_QUEUES')

    CELERY_ROUTES = {
        'worker.task_on_payment': {'queue': 'nft-payment-queue'},
        'worker.task_record_tx': {'queue': 'nft-payment-queue'},
        'worker.task_confirm_tx': {'queue': 'nft-confirm-tx-queue'},
        'worker.task_generate_metadata_file': {'queue': 'nft-tx-queue'},
        'worker.task_create_metadata_file_for_game_item': {'queue': 'nft-metadata-game-item-queue'}
    }
    PUBLIC_PATH = os.getenv('PUBLIC_PATH')
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER'))
    ADDRESS_OF_COUNTER = os.getenv('ADDRESS_OF_COUNTER')
    REDLOCK_REDIS = json.loads(os.getenv('REDLOCK_REDIS', '[]'))
    BSC_RPC_URI = os.getenv('BSC_RPC_URI')
    ETH_RPC_URI = os.getenv('ETH_RPC_URI')
    CHAIN_ID = int(os.getenv('CHAIN_ID'))
    ASSETS = json.loads(os.getenv('ASSETS', '{}'))
    IPFS_TOKEN = os.getenv('IPFS_TOKEN')
    WALLET_IAPI = os.getenv('WALLET_IAPI')
    NFT_ADDRESS = os.getenv('NFT_ADDRESS')
    CREATOR_ADDRESS = os.getenv('CREATOR_ADDRESS')
    BOX_CREATOR_CONTRACT = os.getenv('BOX_CREATOR_CONTRACT')
    CONFIRM_BLOCK = 1
    RECAPTCHA3_PRIVATE_KEY = os.getenv('RECAPTCHA3_PRIVATE_KEY')
    RECAPTCHA_VERIFY_SERVER = 'https://www.google.com/recaptcha/api/siteverify'

    #  Simplex config
    SIMPLEX_URI = os.getenv('SIMPLEX_URI')

    # S3 Config
    S3_HOST = os.getenv("S3_HOST")
    S3_STATIC = os.getenv("S3_STATIC")
    BUCKET_NAME = os.getenv("BUCKET_NAME")
    AWS_SECRET = os.getenv("AWS_SECRET")
    AWS_KEY = os.getenv("AWS_KEY")

    # ChainId for multi-chain mint
    SMC_CHAIN_IDS = json.loads(os.getenv('SMC_CHAIN_IDS', '[]'))