

from models import ItemsModel
import pydash as py_

class ItemsHelper:
    @staticmethod 
    def get_items():
        items = list(ItemsModel.find(
            filter={}
        ))
        return {
            'items':items
        }
    @staticmethod
    def get_items_with_rarity(_rarity):
        items = list(ItemsModel.find(
            filter={
                'rarity': _rarity
            }
        ))
        return {
            'items':items
        }
        