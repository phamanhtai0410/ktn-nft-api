# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import json
import sys

import w3storage

import io

IPFS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGZmZTZENzFjNmFhYUVGODg1NWY2YkU0MDVDYjNjOTBFM0JDMkZEMzciLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NjMwNTMxMTAyMjEsIm5hbWUiOiJzY2FuaHViIn0.RVXqjQKEJ1LhFIjsZXMY5ISs_cgZhuFn8q3zYNfOnWI"
w3 = w3storage.API(
    token=IPFS_TOKEN)
_files = []

for _file in range(0,3):
    _file_io = io.BytesIO(json.dumps({
        'id': _file
    }).encode())
    _file_io.name = f'{_file}.json'
    _files.append(_file_io)


ci = w3.post_car(
 *_files
)
print(ci)
