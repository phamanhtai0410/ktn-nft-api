# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get
from models import CollectionModel
from bson import ObjectId
from pydash import get
from tasks.metadata import task_create_metadata_file_for_game_item

class GameItemMetadataHelper:

    @classmethod
    def gen_metadata_files(self, _collection_id):
        _collection = CollectionModel.find_one(filter={
            "_id": ObjectId(_collection_id)
        })
        _address = get(_collection, "address")
        if not _address:
            raise "No contract address found"
        _types_list = get(_collection, "types_list")
        
        for _item in _types_list:
            _item.pop("rate")
            _item.pop("AssetName")
            _item.pop("AssetDescription")
            _json = {
                "name": get(_item, "AssetName"),
                "image": get(_item, "Image"),
                "description": get(_item, "AssetDescription"),
                "animation_url": get(_item, "AnimationUrl"),
                "attributes": _item
            }
            task_create_metadata_file_for_game_item.delay(
                _json,
                _address
            )
        return {
            "result": "Sucess"
        }
