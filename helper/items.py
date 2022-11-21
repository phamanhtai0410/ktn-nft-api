from models import MeshMaterialModel, MeshModel
from models import CollectionModel
from pydash import get
from datetime import timezone


class ItemsHelper:
    @classmethod
    def get_items(cls, _nft_id, _type, _page, _page_size, _sort):

        _filter = {
            'is_show': True
        }

        def func_filter(item):
            if not _nft_id is None and get(item, 'nft_id') != _nft_id:
                return False
            if not _type is None and get(item, 'type') != _type:
                return False
            return True

        items = MeshMaterialModel.page(
            filter=_filter,
            page=_page,
            page_size=_page_size,
            sort=_sort,
            func_sort=lambda item: get(item, 'created_time'),
            func_filter=func_filter,
            hset_field='nft_id'
        )
        print(items)
        items['items'] = [{
            **x,
            **cls.get_info_of_mesh_material(get(x, 'mesh_id'))
        } for x in items['items']]

        return items

    @classmethod
    def get_info_of_mesh_material(cls, mesh_id):
        _mesh = cls.get_mesh(mesh_id)
        if not _mesh:
            return {}

        return {
            'price': get(_mesh, 'price'),
            'mesh_index': get(_mesh, 'mesh_index'),
            'address': get(_mesh, 'address'),
            'discount': get(_mesh, 'discount'),
            'rarity': get(_mesh, 'rarity'),
            'collection_id': get(_mesh, 'collection_id')
        }

    @staticmethod
    def get_mesh(mesh_id):
        _mesh = MeshModel.find_one({
            'mesh_id': mesh_id
        })
        return _mesh

    @classmethod
    def get_nft_of(cls, _collection_id):
        _collection = CollectionModel.find_one_with_hset(filter={
            'collection_id': _collection_id
        }, hset_field="collection_id")
        return {
            "items": [{
                **x,
                **cls.get_info_of_mesh_material(get(x, 'mesh_id'))
            } for x in cls.get_nfts(get(_collection, 'collection_id', []))],
            'num_of_page': 1,
            'page_size': 20,
            'page': 1
        }

    @classmethod
    def get_collection(cls, _collection_id, _page, _page_size, _sort):
        _filter = {}
        if not _collection_id is None:
            _collection = CollectionModel.find_one_with_hset(filter={
                'collection_id': _collection_id
            }, hset_field="collection_id")
            print('_collection', _collection)
            items = {
                "items": [_collection],
                'num_of_page': 1,
                'page_size': 20,
                'page': 1
            }
        else:
            items = CollectionModel.page(
                filter=_filter,
                page=_page,
                page_size=_page_size,
                sort=_sort,
                func_sort=lambda item: get(item, 'created_time'),
                hset_field='collection_id',
                # cache=True
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
        # _nfts =
        return MeshMaterialModel.find(
            filter={
                'collection_id': collection_id
            }
        )

    @staticmethod
    def get_item_by_rt(address, mesh_index):
        _nft_detail = MeshModel.find_one(
            filter={
                'address': address,
                'mesh_index': mesh_index
            },
            # cache=True
        )
        return _nft_detail
