from datetime import timezone

from pydash import get

from models import NFTsModel


class MyNFTsHelpers:

    @staticmethod
    def get_my_nfts(address: str, page: int, page_size: int, sort: int):
        _results = NFTsModel.page(
            filter={
                'address': address
            },
            page=page,
            page_size=page_size,
            sort=sort,
            func_sort=lambda item: get(item, 'created_time')
        )

        _itemsFormatted = []
        _itemsFormatted = [{
            'token_id': get(_item, 'token_id'),
            'address': get(_item, 'address'),
            'type': get(_item, 'type', default=0),  # Need update later
            'rarity': get(_item, 'rarity'),
            'token_uri': get(_item, 'token_uri'),
            'created_time': get(_item, 'created_time').replace(tzinfo=timezone.utc).timestamp(),
        } for _item in get(_results, 'items')]

        _results['items'] = _itemsFormatted
        return _results
