# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask import request
from flask_restful import Resource
from pydash import get

from connect import security
from helper.captcha import CaptchaHelper
from helper.promo_code import PromoCodeHelper
from lib import BadRequest
from schemas.promo import PromoCodeQuery


class PromoResource(Resource):

    @security.http(
        params=PromoCodeQuery()
    )
    def get(self, params):
        if not CaptchaHelper.validate_recaptcha(response=get(params, 'token'),
                                                remote_addr=request.headers.get('X-Real-Ip'),
                                                action="check_promotion_code"):
            raise BadRequest(msg="Invalid captcha", errors=[{
                'captcha': "Invalid captcha."
            }])
        _discount = PromoCodeHelper.check(get(params, 'code'))
        return {
            'discount': _discount
        }
