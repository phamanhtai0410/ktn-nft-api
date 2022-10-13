# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from bson import ObjectId
items = [{"name": 1}]
for _item in items:
    _item['id'] = 1
print(items)
