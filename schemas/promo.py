# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, fields

from lib import NotBlank


class PromoCodeQuery(Schema):
    class Meta:
        unknown = EXCLUDE

    code = fields.Str(required=True, validate=NotBlank())
    token = fields.Str(required=True, validate=NotBlank())
