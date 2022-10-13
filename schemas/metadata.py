from marshmallow import Schema, EXCLUDE, fields, validate


class ItemSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String()
    image = fields.String()
    description = fields.String()
    rarity = fields.Integer()


class MetaDataSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    promotion_code = fields.String(required=False, default=None)
    items = fields.List(fields.Nested(ItemSchema), required=True, validate=validate.Length(min=1))


class ResMetaDataSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    signature = fields.String(required=True)
    data = fields.Dict(required=True)
