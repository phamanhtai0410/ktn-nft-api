

from bson import ObjectId
from models import NFTDetailModel
from enums.items import Items


class ItemsHelper:
    @staticmethod 
    def get_items():
        items = NFTDetailModel.find(
            filter={}
        )
        return {
            'items':items
        }
    @staticmethod
    def get_items_with_rarity(_rarity):
        items = NFTDetailModel.find(
            filter={
                'rarity': _rarity
            }
        )
        rarity = getattr(Items, _rarity)
        return {
            'items':items,
            'image': rarity['image']
        }
    @staticmethod
    def get_items_with_id(_id):
        item = NFTDetailModel.find_one(
            filter={
                '_id': ObjectId(_id)
            }
        )
        return item

        