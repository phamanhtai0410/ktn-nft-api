from marshmallow import Schema, EXCLUDE, fields, validate

from lib import NotBlank


class MetaDataSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    promotion_code = fields.String(required=False, default=None, allow_none=True)
    address = fields.String(required=True, validate=NotBlank())
    items = fields.List(fields.Integer, required=True, validate=validate.Length(min=1))


class SignatureSchema(Schema):
    class Meta:
        unknown: EXCLUDE

    v = fields.String(required=True)
    r = fields.String(required=True)
    s = fields.String(required=True)

class ResMetaDataSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    signature = fields.Nested(SignatureSchema)
    data = fields.Dict(required=True)
