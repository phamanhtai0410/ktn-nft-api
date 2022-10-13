# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import sys

import w3storage

from config import Config
from lib.logger import debug
import io

w3 = w3storage.API(
    token=Config.IPFS_TOKEN)


class IPFSHelper:
    @staticmethod
    def upload_web3(metadata):
        file = io.BytesIO(json.dumps(metadata).encode())
        _cid = w3.post_upload(file)
        debug(f"https://{_cid}.ipfs.w3s.link")
        return _cid
