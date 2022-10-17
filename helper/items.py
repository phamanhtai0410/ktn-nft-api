from bson import ObjectId
from models import NFTDetailModel
from enums.items import Items
from models import CollectionModel
from lib.exception import BadRequest


class ItemsHelper:
    @staticmethod
    def get_items(_nft_id, _type, _page, _page_size):
        
        _filter = {}
        if not _nft_id is None:
            _filter['nft_id'] = _nft_id
        if not _type is None:
            _filter['type'] = _type    
        items = NFTDetailModel.page(
            filter=_filter,
            page=_page,
            page_size=_page_size
        )
        return items


    @staticmethod
    def get_collection(_collection_id, _page, _page_size):
        _filter = {}
        if not _collection_id is None:
            _filter['collection_id'] = _collection_id
        items = CollectionModel.page(
            filter= _filter, 
            page=_page,
            page_size=_page_size
        )
        return items
