

from distutils.log import error
from bson import ObjectId
from models import NFTDetailModel
from enums.items import Items
from models import CollectionModel
from lib.exception import BadRequest

class ItemsHelper:
    @staticmethod 
    def get_items():
        items = NFTDetailModel.find(
            filter={}
        )
        if not items: 
            raise BadRequest("list nft is null")
        return {
            'items':items
        }
        
    @staticmethod
    def get_collections_list():
        collections = CollectionModel.find(
            filter={}
        )
        if not collections: 
            raise BadRequest("list collection is null")
        return {'collection': collections}   
    @staticmethod
    def get_collection(_collection_id):
        collection = CollectionModel.find(
            filter={
                'collection_id': _collection_id
            }
        )
        if not collection: 
            raise BadRequest("collection_id does not exist.", errors =[{
                'collection_id': 'not found'
            }])
        return {'collection': collection} 
    @staticmethod
    def get_items_with_id(_id):
        item = NFTDetailModel.find_one(
            filter={
                'nft_id': _id
            }
        )
        if not item: 
            raise BadRequest("nft_id does not exist.", errors =[{
                'nft_id': 'not found'
            }])
        return item

        