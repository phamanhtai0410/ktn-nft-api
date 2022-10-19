from models import NFTDetailModel
from models import CollectionModel
from pydash import get
from datetime import timezone


class ItemsHelper:
    @staticmethod
    def get_items(_nft_id, _type, _page, _page_size, _sort):
    
        _filter = {}
        if not _nft_id is None:
            _filter['nft_id'] = _nft_id
        if not _type is None:
            _filter['type'] = _type
        items = NFTDetailModel.page(
            filter=_filter,
            page=_page,
            page_size=_page_size,
            sort=_sort,
            func_sort=lambda item: get(item, 'created_time')
        )
        # _itemsFormatted = []
        # _itemsFormatted = [{
        #     'nft_id': get(_item, 'nft_id'),
        #     'name': get(_item, 'name'),
        #     'rarity': get(_item, 'rarity'),
        #     'type': get(_item, 'type'),
        #     'description': get(_item, 'description'),
        #     'image': get(_item, 'image'),
        #     'price': get(_item, 'price'),
        #     'created_time': get(_item, 'created_time').replace(tzinfo=timezone.utc).timestamp(),
        # } for _item in get(items, 'items')]

        # items['items'] = _itemsFormatted
        return items

    @classmethod
    def get_collection(cls, _collection_id, _page, _page_size, _sort):
        _filter = {}
        if not _collection_id is None:
            _filter['collection_id'] = _collection_id
        items = CollectionModel.page(
            filter=_filter,
            page=_page,
            page_size=_page_size,
            sort=_sort,
            func_sort=lambda item: get(item, 'created_time')
        )
        _itemsFormatted = []
        _itemsFormatted = [{
            'collection_id': get(_item, 'collection_id'),
            'name': get(_item, 'name'),
            'description': get(_item, 'description'),
            'nfts': cls.get_nfts(_item['collection_id']),
            'image': get(_item, 'image'),
            'created_time': get(_item, 'created_time'),
        } for _item in get(items, 'items')]
        items['items'] = _itemsFormatted
        return items

    @staticmethod
    def get_nfts(collection_id):
        _nfts = NFTDetailModel.find(
            filter={
                'type': collection_id
            }
        )
        return _nfts

    @staticmethod
    def get_item(filter_data):
        _nft_detail = NFTDetailModel.find_one(
            filter=filter_data
        )
        return _nft_detail
