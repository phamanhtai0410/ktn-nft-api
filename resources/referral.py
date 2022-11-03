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
from helper.metadata import MetaDataHelper
from lib import BadRequest
from schemas.referral import ReferralCodeQuery


class ReferralResource(Resource):

    @security.http(
        params=ReferralCodeQuery()
    )
    def get(self, params):
        # if not CaptchaHelper.validate_recaptcha(
        #         response=get(params, 'token'),
        #         remote_addr=request.headers.get('X-Real-Ip'),
        #         action="check_ref_code"
        # ):
        #     raise BadRequest(
        #         msg="Invalid captcha",
        #         errors=[{
        #             'captcha': "Invalid captcha."
        #         }]
        #     )

        _ref_code = get(params, 'code')

        MetaDataHelper.check_ref_code(ref_code=_ref_code)
        return {
            'status': "valid"
        }
