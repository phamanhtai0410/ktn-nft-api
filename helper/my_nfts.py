from datetime import timezone, datetime

from pydash import get
from enums.nft import NFTType

from helper.items import ItemsHelper
from lib import dt_utcnow
from models import NFTsModel


class MyNFTsHelpers:

    @staticmethod
    def get_my_nfts(address: str, page: int, page_size: int, sort: int, nft_type: str = ''):
        _results = NFTsModel.page(
            filter={
                'address': address
            },
            page=page,
            page_size=page_size,
            sort=sort,
            func_sort=lambda item: get(item, 'created_time', default=dt_utcnow()),  # need update
            # cache=False,
            func_filter=lambda x: get(x, 'nft_type') == nft_type if nft_type else True
        )
        _items_formatted = []
        for _item in get(_results, 'items'):
            _nft_detail = None
            if get(_item, 'nft_type') == NFTType.NFT:
                _nft_detail = ItemsHelper.get_item_by_rt(
                    address=get(_item, 'contract'),
                    mesh_index=get(_item, 'mesh_index')
                )
                print('_nft_detail', _nft_detail)
                if not _nft_detail:
                    continue

                _nft_detail = {
                    **_nft_detail,
                    **ItemsHelper.get_info_of_mesh_material(get(_nft_detail, 'mesh_id'))
                }

            _item_detail = {
                'token_id': get(_item, 'token_id'),
                'address': get(_item, 'address'),
                'contract': get(_item, 'contract'),
                'nft_type': get(_item, 'nft_type', default=''),  # Need update later
                'rarity': get(_item, 'rarity', default=0),
                'mesh_material': get(_item, 'mesh_material', default=0),
                'mesh_index': get(_item, 'mesh_index', default=0),
                'is_opened': get(_item, 'is_opened', default=False),
                'name': get(_nft_detail, 'name', default=''),
                'price': get(_nft_detail, 'price', default=0) if get(_item, 'nft_type') == NFTType.NFT else get(_item, 'price', default=0),
                'description': get(_nft_detail, 'description', default=''),
                'image': get(
                    _nft_detail,
                    'image',
                    default='https://ipfs.io/ipfs/bafybeiaw62gms2uo7ioi4wmuhonupb5hxfemogkcoajjaiok55yjp44a4a/'
                ),
                'is_staking': get(_item, 'is_staking', default=False),
                'token_uri': get(_item, 'token_uri', default=''),
                'created_time': get(_item, 'created_time').replace(tzinfo=timezone.utc).timestamp()
            }
            _items_formatted.append(_item_detail)

        _results['items'] = _items_formatted
        return _results
