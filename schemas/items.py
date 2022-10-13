# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate
from enums.items import Items
from lib.schema import ObjectIdField


class ItemsResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    name = fields.String(default='', missing='')
    rarity = fields.String(default='', missing='')
    description = fields.String(default='', missing='')
    image = fields.String(default='', missing='')
    price = fields.Float(default=0, missing=0)


class ItemsListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(ItemsResponseSchema))


class ItemsRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE

    rarity = fields.String(validate=validate.OneOf([
        Items.UNCOMMON,
        Items.RARE,
        Items.MYTHICAL,
        Items.LEGENDARY,
        Items.IMMORTAL
    ]))
    _id = fields.String()



