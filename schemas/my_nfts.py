from marshmallow import Schema, EXCLUDE, fields, RAISE, validate
from enums.nft import NFTType

from lib import NotBlank


class MyNFTsRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    address = fields.Str(required=True, validate=NotBlank())
    nft_type = fields.String(required=False, validate=validate.OneOf([
        NFTType.BOX,
        NFTType.NFT
    ]))
    token_ids = fields.String(default='')
    contract = fields.String(default='')
    page = fields.Integer(required=False, default=1)
    page_size = fields.Integer(required=False, default=10)
    sort = fields.String(required=False, default='desc')


class NFTResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    token_id = fields.Integer(required=True, default=None)
    address = fields.String(required=True, default=None)
    name = fields.String(required=True, default=None)
    description = fields.String(required=True, default=None)
    image = fields.String(required=True, default=None)
    nft_type = fields.String(required=True, default='')
    contract = fields.String(required=True, default='')
    mesh_material = fields.Integer(required=False, default=0)
    mesh_index = fields.Integer(required=False, default=0)
    is_opened = fields.Boolean(required=False, default=False)
    price = fields.Float(required=True, default=0)
    rarity = fields.Integer(required=False, default=0, missing=0)
    token_uri = fields.String(required=True)
    is_staking = fields.Boolean(required=False, default=False, missing=False)
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
