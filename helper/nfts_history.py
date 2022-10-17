from bson import ObjectId
from datetime import timezone

from pydash import get
from models import NFTsHistoryModel
from lib.exception import BadRequest

class NFTsHistoryHelper:
    @staticmethod 
    def get_history(_token_id, _page, _page_size, _sort):
        if not _token_id:
            _filter= {}
        else: 
            _filter = {
            'token_id' : _token_id
        }
        _results = NFTsHistoryModel.page(
            filter= _filter,
            page=_page,
            page_size=_page_size,
            sort=_sort,
            func_sort=lambda item: get(item, 'block_time')
        )
        _itemsFormatted = []
        _itemsFormatted = [{
            'from_address': get(_item, 'from_address'),
            'to_address': get(_item, 'to_address'),
            'token_id': get(_item, 'token_id'),
            'event': get(_item, 'event'),
            'tx_hash': get(_item, 'tx_hash'),
            'block_number': get(_item, 'block_number'),
            'block_time': get(_item, 'block_time'),
            'created_time': get(_item, 'created_time').replace(tzinfo=timezone.utc).timestamp(),
            'created_by': get(_item, 'created_by'),
        } for _item in get(_results, 'items')]

        _results['items'] = _itemsFormatted
        
        return _results