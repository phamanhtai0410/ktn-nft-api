# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import requests

from config import Config


class SimplexHelper:

    @staticmethod
    def open(url, *args, **kwargs):
        response = requests.request(
            **kwargs,
            url=f'{Config.SIMPLEX_URI}/{url}'
        )
        return response

    @classmethod
    def quote(cls, end_user_id, amount):
        _quote_data = {
            "end_user_id": end_user_id,
            "digital_currency": "USDT",
            "fiat_currency": "USD",
            "requested_currency": "USD",
            "requested_amount": amount,
            "wallet_id": "partner_name",
            "client_ip": "1.2.3.4"
        }
        _res = cls.open(
            '/wallet/merchant/v2/quote',
            json=_quote_data
        )

        if _res.status_code != 200:
            return None

        return _res.json()

