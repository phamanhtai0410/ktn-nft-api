# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import sentry_sdk
from pydash import get

from enums.order import Status
from lib import DaoModel, dt_utcnow


class OrderDao(DaoModel):

    def __init__(self, *args, **kwargs):
        super(OrderDao, self).__init__(*args, **kwargs)
