# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields


class BoxSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    address = fields.String(missing='')
    end_date = fields.Float(missing=0)
    price = fields.Float(missing=0)
    name = fields.String(missing='')
