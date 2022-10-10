# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
# from helper.sync import sync_task
from worker import worker


@worker.task(name='worker.task_hello', rate_limit='1000/s')
def task_hello():
    return ""


@worker.task(name='worker.sync_task_hello', rate_limit='1000/s')
# @sync_task
async def sync_task_hello():
    return ""
