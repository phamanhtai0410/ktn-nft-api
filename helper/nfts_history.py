from bson import ObjectId
from models import NFTsHistoryModel
from lib.exception import BadRequest

class NFTsHistoryHelper:
    @staticmethod 
    def get_history(_token_id):
        items = NFTsHistoryModel.find(
            filter={}
        )
        if not items: 
            raise BadRequest("list nft is null")
        return {
            'items':items
        }