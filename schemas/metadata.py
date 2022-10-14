from marshmallow import Schema, EXCLUDE, fields, validate

from lib import NotBlank


class ItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String()
    image = fields.String()
    description = fields.String()
    rarity = fields.Integer()
    type = fields.Integer()


class MetaDataSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    promotion_code = fields.String(required=False, default=None)
    address = fields.String(required=True, validate=NotBlank())
    items = fields.List(fields.Nested(ItemSchema), required=True, validate=validate.Length(min=1))


class ResMetaDataSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    signature = fields.String(required=True)
    data = fields.Dict(required=True)
