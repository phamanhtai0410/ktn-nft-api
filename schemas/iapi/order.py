# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields


class ResultOrderSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    order_id = fields.Str(required=True)
    tx_hash = fields.Str(required=True)
    token_ids = fields.List(fields.Dict(), missing=[])
    address = fields.Str(required=True)

