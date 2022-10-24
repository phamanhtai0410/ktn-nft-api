# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from pydash import get

from lib import NotFound
from models import PromotionCodeModel


class PromoCodeHelper:

    @staticmethod
    def check(code):
        _code = PromotionCodeModel.find_one({
            'code': code
        })
        if not get(_code, 'status'):
            raise NotFound()

        return get(_code, 'discount', 0)
