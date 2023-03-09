# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields


class GameItemForm(Schema):
    class Meta:
        unknown = RAISE

    collection_id = fields.Str(required=True)


class GameItemMetadataResp(Schema):
    class Meta:
        unknown = EXCLUDE

    result = fields.Str(required=True)