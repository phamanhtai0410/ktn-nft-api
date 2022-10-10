

from models import ItemModel
import pydash as py_

class ItemsHelper:
    @staticmethod 
    def get_items():
        items = list(ItemModel.find(
            filter={}
        ))
        return {
            'items':items
        }
    @staticmethod
    def get_items_with_rarity(_rarity):
        items = list(ItemModel.find(
            filter={
                'rarity': _rarity
            }
        ))
        return {
            'items':items
        }
        