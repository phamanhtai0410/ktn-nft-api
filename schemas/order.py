# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields, validate

from enums.order import Units, Chains
from lib import NotBlank, ObjectIdField, IsObjectId


class ItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    nft_id = fields.Int(required=True)
    amount = fields.Int(required=True, validate=validate.Range(min=1))


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
    promotion_code = fields.Str(default='', allow_none=True)
    ref_code = fields.Str(allow_none=True)


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
    discount = fields.Float(missing=0)
    deadline = fields.Float()


class PaymentSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    order_id = fields.UUID(required=True)
    tx_hash = fields.Str(required=True, validate=NotBlank())


class ResPaymentSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    order_id = fields.Str(required=True)
    tx_hash = fields.Str(required=True)
    status = fields.Str(required=True)
