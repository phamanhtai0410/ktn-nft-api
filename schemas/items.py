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
    nft_id   = fields.Integer(required=True)
class ItemResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    nft_id = fields.Integer(default='',missing='')
    name = fields.String(default='', missing='')
    rarity = fields.Integer(default='',missing='')
    type = fields.Integer(default='',missing='')
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
        
    # rarity = fields.Integer(validate=validate.OneOf([
    #     Items.UNCOMMON,
    #     Items.RARE,
    #     Items.MYTHICAL,
    #     Items.LEGENDARY,
    #     Items.IMMORTAL
    # ]))
    collection_id = fields.Integer(required=False)
    

class CollectionResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    collection_id = fields.Integer(default='',missing='')
    collection_name  = fields.String(default='',missing='')
    collection_description = fields.String(default='',missing='')
    collection_rarity = fields.String(default='',missing='')   
    items = fields.List(fields.Nested(ItemResponseSchema))
    collection_image = fields.String(default='',missing='')

class CollectionListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    
    collection  = fields.List(fields.Nested(CollectionResponseSchema))
    

        
    
    
