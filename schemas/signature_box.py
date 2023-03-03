from marshmallow import Schema, EXCLUDE, fields, validate

from lib import NotBlank


class SignatureBoxSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    promotion_code = fields.String(required=False, default=None, allow_none=True)
    ref_code = fields.String(required=False, default=None, allow_none=True)
    address = fields.String(required=True, validate=NotBlank())
    amount = fields.Int(required=True, validate=validate.Range(min=1))
    is_whitelist_mint = fields.Bool(required=True)


class ResSignatureBoxSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    signature = fields.String(required=True)
    callback = fields.String(required=True)
    data = fields.Dict(required=True)
