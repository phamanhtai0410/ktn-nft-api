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

    name = fields.String(default='', missing='')
    rarity_code = fields.String(default='',missing='')
    description = fields.String(default='',missing='')
    image = fields.String(default='',missing='')
    price = fields.Float(default='',missing='')

class ItemsListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    items = fields.List(fields.Nested(ItemsResponseSchema))

class ItemsRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    rarity_code = fields.String(required=False)
        
    
    
