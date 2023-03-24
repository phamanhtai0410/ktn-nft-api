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
        if not _code:
            raise NotFound()
        if get(_code, 'used', 0) >= get(_code, 'total', 0):
            raise NotFound()
        return get(_code, 'discount', 0)
