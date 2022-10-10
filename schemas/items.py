# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class ItemsResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    item_id = fields.String(default='', missing='')
    name = fields.String(default='', missing='')
    rarity = fields.String(default='',missing='')
    image = fields.String(default='',missing='')
    price = fields.String(default='',missing='')

class ItemsListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    items = fields.List(fields.Nested(ItemsResponseSchema))

class ItemsRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    rarity = fields.String(required=False)
        
    
    
