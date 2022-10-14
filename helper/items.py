
from bson import ObjectId
from models import NFTDetailModel
from enums.items import Items
from models import CollectionModel
from lib.exception import BadRequest

class ItemsHelper:
    @staticmethod 
    def get_items(_page , _page_size):
        items = NFTDetailModel.page(
            filter={},
            page=_page,
            page_size=_page_size           
        )
        return items
        
    @staticmethod
    def get_collections_list(_page , _page_size):
        items = CollectionModel.page(
            filter={},
            page=_page,
            page_size=_page_size   
        )
        return items
    @staticmethod
    def get_collection(_collection_id, _page , _page_size):
        items = CollectionModel.page(
            filter={
                'collection_id': _collection_id
            },
            page=_page,
            page_size=_page_size   
        )
        return items
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

        