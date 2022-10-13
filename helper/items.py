
from bson import ObjectId
from models import NFTDetailModel
from enums.items import Items
from models import CollectionModel

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
    def get_collections_list():
        collections = CollectionModel.find(
            filter={}
        )
        if not collections: return {}
        return {'collection': collections}   
    @staticmethod
    def get_collection(_collection_id):
        collection = CollectionModel.find(
            filter={
                'collection_id': _collection_id
            }
        )
        if not collection: return {}
        return {'collection': collection} 
    @staticmethod
    def get_items_with_id(_id):
        item = NFTDetailModel.find_one(
            filter={
                'nft_id': _id
            }
        )
        return item

        