# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate
from enums.items import Items
from lib.schema import ObjectIdField, DatetimeField


class ItemResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    nft_id = fields.Integer(default=0, missing=0)
    name = fields.String(default='', missing='')
    rarity = fields.Integer(default=0, missing=0)
    type = fields.Integer(default=0, missing=0)
    description = fields.String(default='', missing='')
    image = fields.String(default='', missing='')
    price = fields.Float(default=0, missing=0)
    discount = fields.Float(missing=0)
    created_time = DatetimeField(required=0, missing=0)
    address = fields.String(default='', allow_none=True)


class ItemsListRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    nft_id = fields.Integer(required=False)
    type = fields.Integer(required=False)
    page = fields.Integer(required=False, default=1)
    page_size = fields.Integer(required=False, default=10)
    sort = fields.String(required=False, default='desc')


class ItemsListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(ItemResponseSchema))
    num_of_page = fields.Integer(data_key='num_of_page', missing=0)
    page_size = fields.Integer(data_key='page_size', missing=10)
    page = fields.Integer(data_key='page', missing=1)


class CollectionRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE

    collection_id = fields.Integer(required=False)
    page = fields.Integer(required=False, default=1)
    page_size = fields.Integer(required=False, default=10)
    sort = fields.String(required=False, default='desc')


class CollectionResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    collection_id = fields.Integer(default=0, missing=0)
    name = fields.String(default='', missing='')
    description = fields.String(default='', missing='')
    nfts = fields.List(fields.Nested(ItemResponseSchema), missing=[])
    image = fields.String(default='', missing='')
    created_time = DatetimeField(required=0, missing=0)
    address = fields.String(default='', allow_none=True)


class CollectionListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(CollectionResponseSchema))
    num_of_page = fields.Integer(data_key='num_of_page', missing=0)
    page_size = fields.Integer(data_key='page_size', missing=10)
    page = fields.Integer(data_key='page', missing=1)


class ItemsShowRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    # is_show = fields.Boolean(required=True)
    page = fields.Integer(required=False, default=1)
    page_size = fields.Integer(required=False, default=10)
    sort = fields.String(required=False, default='desc')
