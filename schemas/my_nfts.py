from marshmallow import Schema, EXCLUDE, fields, RAISE

from lib import NotBlank


class MyNFTsRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    address = fields.Str(required=True, validate=NotBlank())
    page = fields.Integer(required=False, default=1)
    limit = fields.Integer(required=False, default=10)
    arrange = fields.String(required=False, default='desc')

class NFTResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    token_id = fields.Integer()
    address = fields.String()
    type = fields.Integer()
    rarity = fields.Integer()
    token_uri = fields.String()
    created_time = fields.DateTime()


class MyNFTsResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    my_nfts = fields.List(fields.Nested(NFTResponseSchema), data_key='my_nfts', missing=[])
    skip = fields.Integer(data_key='skip', missing=0)
