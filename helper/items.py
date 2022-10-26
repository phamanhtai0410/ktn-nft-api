from models import NFTDetailModel
from models import CollectionModel
from pydash import get
from datetime import timezone


class ItemsHelper:
    @staticmethod
    def get_items(_nft_id, _type, _page, _page_size, _sort):

        _filter = {
            'is_show': True
        }

        def func_filter(item):
            if not _nft_id is None and get(item, 'nft_id') != _nft_id:
                return False
            if not _type is None and get(item, 'type') != _type:
                return False
            return True

        items = NFTDetailModel.page(
            filter=_filter,
            page=_page,
            page_size=_page_size,
            sort=_sort,
            func_sort=lambda item: get(item, 'created_time'),
            func_filter=func_filter,
            cache=True,
            hset_field='nft_id'
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
            func_sort=lambda item: get(item, 'created_time'),
            hset_field='collection_id',
            cache=True
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
                'type': collection_id,
                'is_show': True
            },
            cache=True,
            hset_field='type'
        )
        return _nfts

    @staticmethod
    def get_item_by_rt(nft_type, rarity):
        _nft_detail = NFTDetailModel.find_one(
            filter={
                'type': nft_type,
                'rarity': rarity
            },
            cache=True
        )
        return _nft_detail

    @staticmethod
    def get_item_by_id(nft_id):
        _nft_detail = NFTDetailModel.find_one(
            filter={
                'nft_id': nft_id,
                'is_show': True
            },
            cache=True
        )
        return _nft_detail

    @staticmethod
    def get_items_show(_page, _page_size, _sort):
        items = NFTDetailModel.page(
            filter={
                'is_show': True
            },
            page=_page,
            page_size=_page_size,
            sort=_sort,
            func_sort=lambda item: get(item, 'created_time'),
            cache=True
        )
        return items
