# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from email.policy import default
from venv import create
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate
from lib.schema import ObjectIdField, DatetimeField


class NFTsHistoryRequestParams(Schema):
    class Meta:
        unknown = EXCLUDE        
    token_id = fields.Integer(required=False)
    page = fields.Integer(required=False, default=1)
    page_size = fields.Integer(required=False, default=10)
    sort = fields.String(required=False, default='desc')
class NFTsHistoryResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    from_address = fields.String(default='',missing='')
    to_address = fields.String(default='',missing='')
    token_id = fields.Integer(default=0,missing=0)
    event = fields.String(default='',missing='')
    tx_hash = fields.String(default='',missing='')
    block_number = fields.Integer(default=0,missing=0)
    block_time  = fields.Integer(default=0,missing=0)
    created_time = DatetimeField(default=0,missing=0)
    created_by = fields.String(default='',missing='')
    
class NFTsHistoryListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True
    items = fields.List(fields.Nested(NFTsHistoryResponseSchema))
    num_of_page = fields.Integer(data_key='num_of_page', missing=0)
    page_size = fields.Integer(data_key='page_size', missing=10)
    page = fields.Integer(data_key='page', missing=1)