# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from models import BoxModel


class BoxHelper:

    @staticmethod
    def active():
        return BoxModel.find_one({
            'active': True
        })

    @staticmethod
    def by_id(box_id):
        return BoxModel.find_one({
            'box_id': box_id
        })
