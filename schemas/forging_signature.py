from marshmallow import Schema, fields, RAISE, EXCLUDE


class ForgingSignatureRequestSchema(Schema):
    class Meta:
        unknown = RAISE

    chain_id = fields.Integer(required=True)
    user_address = fields.String(required=True)
    collection_address = fields.String(required=True)
    collection_addresses_forging = fields.List(fields.String, required=True)
    token_ids_forging = fields.List(fields.Integer, required=True)
    nft_indexes_forging = fields.List(fields.Integer, required=True)


class ForgingSignatureResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    signature = fields.String(required=True)
    callback = fields.String(required=True)
    data = fields.Dict(required=True)
