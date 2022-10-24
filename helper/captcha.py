# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import traceback

import requests
import sentry_sdk
from flask import request
from pydash import get

from config import Config
from lib import BadRequest
from lib.logger import debug

RECAPTCHA_ERROR_CODES = {
    'missing-input-secret': 'The secret parameter is missing.',
    'invalid-input-secret': 'The secret parameter is invalid or malformed.',
    'missing-input-response': 'The response parameter is missing.',
    'invalid-input-response': 'The response parameter is invalid or malformed.'
}


class CaptchaHelper:
    @staticmethod
    def validate_recaptcha(response, remote_addr, action):
        """Performs the actual validation."""
        # try:
        #     private_key = Config.RECAPTCHA3_PRIVATE_KEY
        # except KeyError:
        #     raise RuntimeError("RECAPTCHA3_PRIVATE_KEY is not set in app config.")

        data = {
            'secret': Config.RECAPTCHA3_PRIVATE_KEY,
            'remoteip': remote_addr,
            'response': response
        }
        debug(f"Check captcha {data}")
        http_response = requests.post(Config.RECAPTCHA_VERIFY_SERVER, data, timeout=10)
        if http_response.status_code != 200:
            return False
        debug(f"Res check captcha {http_response.text}")

        json_resp = http_response.json()
        if get(json_resp, 'success') and get(json_resp, 'action') == action:
            debug(json_resp)
            return True
        else:
            debug(json_resp)

        for error in json_resp.get("error-codes", []):
            if error in RECAPTCHA_ERROR_CODES:
                raise BadRequest(errors={
                    'captcha': RECAPTCHA_ERROR_CODES[error]
                })

        return False
