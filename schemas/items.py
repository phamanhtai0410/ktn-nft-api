# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate
from enums.items import Items
from lib.schema import ObjectIdField


class ItemRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE        
    _id   = fields.String(required=True)
class ItemResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    name = fields.String(default='', missing='')
    rarity = fields.String(default='',missing='')
    description = fields.String(default='',missing='')
    image = fields.String(default='',missing='')
    price = fields.Float(default=0,missing=0)

class ItemsListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    items = fields.List(fields.Nested(ItemResponseSchema))

class CollectionRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE
        
    rarity = fields.String(required = True, validate=validate.OneOf([
        Items.UNCOMMON['type'],
        Items.RARE['type'],
        Items.MYTHICAL['type'],
        Items.LEGENDARY['type'],
        Items.IMMORTAL['type']
    ]))
    

class CollectionResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    items = fields.List(fields.Nested(ItemResponseSchema))
    image = fields.String(default='',missing='')
    

        
    
    
