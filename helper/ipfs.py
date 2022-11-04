# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import w3storage
from pydash import get

from config import Config
from helper.async_request import AsyncHelper
from lib.logger import debug
import io

w3 = w3storage.API(
    token=Config.IPFS_TOKEN)


class IPFSHelper:
    @staticmethod
    def upload_web3(metadata):
        # if Config.DEBUG:
        #     return "abcasdasdaoqowieqojkasfjaksjfasdasdklasdaljdaklsjdadj"
        file = io.BytesIO(json.dumps(metadata).encode())
        _cid = w3.post_upload(file)
        debug(f"https://{_cid}.ipfs.w3s.link")
        return _cid\


    @staticmethod
    async def upload_web3_async(metadata):
        file = io.BytesIO(json.dumps(metadata).encode())
        files = [('file', file)]

        _res = await AsyncHelper.post('https://api.web3.storage/upload',
                                      headers={
                                          "Authorization": f'Bearer {Config.IPFS_TOKEN}'
                                      },
                                      data={
                                          'files': files
                                      })
        _json = await _res.json()

        return get(_json, 'cid')
