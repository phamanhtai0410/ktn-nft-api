from models import NFTsModel


class MyNFTsHelpers:

    @staticmethod
    def get_my_nfts(address: str, limit: int, offset: int, arrange: int):
        results = NFTsModel.col.aggregate([
            {
                '$match': {
                    'address': address
                }
            },
            {
                "$sort": {
                    "created_time": arrange
                }
            },
            {
                '$skip': offset
            },
            {
                '$limit': limit
            }
        ])

        if results is None:
            return []

        return results
