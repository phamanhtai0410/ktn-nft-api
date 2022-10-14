# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from email.policy import default
from venv import create
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate
from lib.schema import ObjectIdField


class NFTsHistoryRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE        
    token_id = fields.Integer(required=True)
class NFTsHistoryResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    _id = ObjectIdField()
    from_address = fields.String(default='',missing='')
    to_address = fields.String(default='',missing='')
    token_id = fields.Integer(default=0,missing=0)
    event = fields.String(default='',missing='')
    tx_hash = fields.String(default='',missing='')
    block_number = fields.Integer(default=0,missing=0)
    block_time  = fields.Float(default=0,missing=0)
    created_time = fields.Date(default='',missing='')
    created_by = fields.String(default='',missing='')