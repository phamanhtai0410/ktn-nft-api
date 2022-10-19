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
        return _results