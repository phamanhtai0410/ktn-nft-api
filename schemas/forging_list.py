from marshmallow import Schema, fields, RAISE, validate, EXCLUDE

from lib import NotBlank, ListChainsSupport, DatetimeField


class ForgingListRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    address = fields.Str(required=True, validate=NotBlank())
    chain = fields.Str(required=True, validate=validate.OneOf(ListChainsSupport))
    collection_type = fields.Str(required=True, validate=validate.OneOf([
        "2D",
        "3D"
    ]))


class ForgingNFTAvailableSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    contract = fields.String(required=True)
    address = fields.String(required=True)
    token_id = fields.Integer(required=True)
    nft_index = fields.Integer(required=True)
    chain = fields.String(required=True)
    token_uri = fields.String(required=True)
    created_time = DatetimeField(required=0, missing=0)


class ForgingListResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        ordered = True

    items = fields.List(fields.Nested(ForgingNFTAvailableSchema()), data_key='items', missing=[])