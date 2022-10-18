from datetime import timezone

from pydash import get

from helper.items import ItemsHelper
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
        _items_formatted = []
        for _item in get(_results, 'items'):
            _nft_detail = ItemsHelper.get_item(
                filter_data={
                    'nft_type': get(_item, 'nft_type'),
                    'rarity': get(_item, 'rarity')
                }
            )
            _item_detail = {
                'token_id': get(_item, 'token_id'),
                'address': get(_item, 'address'),
                'nft_type': get(_item, 'nft_type', default=0),  # Need update later
                'rarity': get(_item, 'rarity'),
                'name': get(_nft_detail, 'name', default=''),
                'price': get(_nft_detail, 'price', default=0),
                'description': get(_nft_detail, 'description', default=''),
                'image': get(_nft_detail, 'image', default=''),
                'is_staking': get(_item, 'image', default=False),
                'token_uri': get(_item, 'is_staking', default=''),
                'created_time': get(_item, 'created_time').replace(tzinfo=timezone.utc).timestamp(),
            }
            _items_formatted.append(_item_detail)

        _mockup_data = [
            {
                'token_id': 1,
                'address': address,
                'nft_type': 0,
                'rarity': 102,
                'name': 'Super Hero',
                'price': 400,
                'description': 'NFT',
                'image': 'https://ipfs.io/ipfs/bafybeieelr4cqukve3mrmwu2nzlou6arl2wcoaaszzanvb3kiif74jzmii',
                'token_uri': '',
                'created_time': 1665807617,
            }
        ]
        if not _items_formatted:
            _results['items'] = _mockup_data
        else:
            _results['items'] = _items_formatted
        return _results
