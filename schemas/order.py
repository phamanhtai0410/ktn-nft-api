# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate

from enums.order import Units, Chains
from lib import NotBlank


class ItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    _id = fields.Str()


class OrderSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    items = fields.List(fields.Nested(ItemSchema), required=True, validate=validate.Length(min=1))
    address = fields.Str(required=True, validate=NotBlank())
    unit = fields.Str(required=True, validate=validate.OneOf([
        Units.BNB,
        Units.USDT,
        Units.ETH
    ]))
    chain = fields.Str(required=True, validate=validate.OneOf([
        Chains.BSC_CHAIN,
        Chains.ETHEREUM_CHAIN
    ]))


class ResOrderSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    order_id = fields.Str()
    cost = fields.Float()

    unit = fields.Str(required=True, validate=validate.OneOf([
        Units.BNB,
        Units.USDT,
        Units.ETH
    ]))

    chain = fields.Str(required=True, validate=validate.OneOf([
        Chains.BSC_CHAIN,
        Chains.ETHEREUM_CHAIN
    ]))

    address_of_counter = fields.Str(required=True)
