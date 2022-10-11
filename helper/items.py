

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
    def get_items_with_rarity(_rarity_code):
        items = list(ItemsModel.find(
            filter={
                'rarity_code': _rarity_code
            }
        ))
        return {
            'items':items
        }
        