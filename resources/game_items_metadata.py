# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from helper.game_item_metadata import GameItemMetadataHelper
from schemas.game_item_metadata import GameItemForm, GameItemMetadataResp
from pydash import get

class GameItemMetadataResource(Resource):

    @security.http(
        form_data=GameItemForm(),
        response=GameItemMetadataResp()
    )
    def post(self, form_data):
        return GameItemMetadataHelper.gen_metadata_files(get(form_data, "collection_id"))

