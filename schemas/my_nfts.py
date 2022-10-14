from marshmallow import Schema, EXCLUDE, fields, RAISE

from lib import NotBlank


class MyNFTsRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    address = fields.Str(required=True, validate=NotBlank())
    page = fields.Integer(required=False, default=1)
    limit = fields.Integer(required=False, default=10)
    sort = fields.String(required=False, default='desc')


class NFTResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    token_id = fields.Integer(required=True, default=None)
    address = fields.String(required=True, default=None)
    type = fields.Integer(required=False, default='')
    rarity = fields.Integer(required=True, default=None)
    token_uri = fields.String(required=True, default=None)
    created_time = fields.Integer(required=True, default=None)


class MyNFTsResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    # {
    #     "items": result,
    #     'num_of_page': num_of_page,
    #     'page_size': page_size,
    #     'page': page
    # }
    items = fields.List(fields.Nested(NFTResponseSchema), data_key='items', missing=[])
    num_of_page = fields.Integer(data_key='num_of_page', missing=0)
    page_size = fields.Integer(data_key='page_size', missing=10)
    page = fields.Integer(data_key='page', missing=1)
