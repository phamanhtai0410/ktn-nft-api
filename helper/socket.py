# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import requests

from connect import socket_io
from lib.logger import debug


class SocketEmitter:

    @staticmethod
    def open(url, *args, **kwargs):
        response = requests.request(
            **kwargs,
            url=url
        )
        print(response.status_code)
        return response.json()

    @staticmethod
    def emit(room_id, event, value):
        debug(f'{value}')
        socket_io.In(room_id).Emit(event, value)
