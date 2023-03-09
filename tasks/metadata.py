# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

import sentry_sdk
from pydash import get
from worker import worker
import models as models
from connect import s3
import traceback
from pathlib import Path
import os
import json
from config import Config

def get_path(filename: str, contract_address: str, folder='metadata'):
    return f'{folder}/{contract_address}/{filename}'

@worker.task(name='worker.task_create_metadata_file_for_game_item', rate_limit='1000/s')
def task_create_metadata_file_for_game_item(
    _metadata_dict: dict,
    _contract_address: str
):
    try:
        _contract_address = _contract_address.lower()
        _asset_id = get(_metadata_dict, "attributes")["AssetID"]
        filename = f"{_asset_id}.json"
        Path(f'metadata/{_contract_address}').mkdir(parents=True, exist_ok=True)
        metadata = _metadata_dict

        with open(os.path.join('metadata', _contract_address, filename), 'w+') as _file:
            _file.write(json.dumps(metadata))
        
        def upload_callback(size, **args):    
            print(size)
            print(args)

        path = get_path(filename, _contract_address, folder="metadata")

        s3.upload_file(
            os.path.join('metadata', _contract_address, filename),
            Bucket=Config.BUCKET_NAME,
            Key=path,
            Callback=upload_callback,
            ExtraArgs={
                "ContentType": "application/json"
            }
        )
            
        return f"Done: Generate metadata file for data => # {Config.S3_STATIC}/{path}"
    except:
        sentry_sdk.capture_exception()
        traceback.print_exc()
        return f"Failed: Generate metadata file for data => #{_metadata_dict}"
