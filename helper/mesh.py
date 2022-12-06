# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from models import MeshModel, MeshMaterialModel


class MeshHelper:

    @staticmethod
    def get_mesh_by_id(mesh_id):
        return MeshModel.find_one(
            filter={
                'mesh_id': mesh_id
            }
        )

    @staticmethod
    def get_mesh_material_by_nft_id(nft_id):
        return MeshMaterialModel.find_one(
            filter={
                'nft_id': nft_id
            }
        )
