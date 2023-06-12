# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pathlib import Path
import boto3
import json
from config import Config
import os
from connect import s3, redis_cluster
# _contract_address = "0x00"
# _asset_id = 1
# filename = f"{_asset_id}.json"
# Path(f'metadata/{_contract_address}').mkdir(parents=True, exist_ok=True)
# _json = {
#     "test_json": 1
# }
# def get_path(filename: str, contract_address: str, folder='nft'):
#     return f'{folder}/{contract_address}/{filename}'
# def upload_callback(size, **args):    
#     print(size)
#     print(args)

# with open(os.path.join('metadata', _contract_address, filename), 'w+') as _file:
#     _file.write(json.dumps(_json))

# path = get_path(filename, _contract_address, folder="metadata")
# response = s3.upload_file(
#     os.path.join('metadata', _contract_address, filename),
#     Bucket="static.katanainu.com",
#     Key=path,
#     Callback=upload_callback,
#     ExtraArgs={
#         "ContentType": "application/json"
#     }
# )
# print('Resp = ', response)

# print(f"Done: Generate metadata file for data => # {Config.S3_STATIC}/{path}")

_key = f'test.nonce'
_nonce = redis_cluster.incr(name=_key, amount=1)
print("* Nonce = ", _nonce)