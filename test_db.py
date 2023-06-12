from helper.metadata import MetaDataHelper

_collection = "0x30b42d199aeceaefeae636f44662e1aa6d147f53".lower()
_address = "0x97f27c48a998E72cf9dEa678c984BF66a6Df3f2C".lower()

_total = MetaDataHelper.count_nft_minted_in_period(
    collection_address=_collection,
    address=_address,
    start_time=1683907200,
    end_time=9999999999
)
print(_total)