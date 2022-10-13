
from bson import ObjectId
from models import NFTDetailModel


class ItemsHelper:
    @staticmethod
    def get_items():
        items = list(NFTDetailModel.find(
            filter={}
        ))
        return {
            'items' :items
        }
    @staticmethod
    def get_items_with_rarity(_rarity):
        items = list(NFTDetailModel.find(
            filter={
                'rarity': _rarity
            }
        ))
        return {
            'items' :items
        }
    @staticmethod
    def get_items_with_id(_id):
        items = list(NFTDetailModel.find(
            filter={
                '_id': ObjectId(_id)
            }
        ))
        return {
            'items' :items
        }
