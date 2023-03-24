# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from lib import DaoModel, dt_utcnow


class PromotionCodeDao(DaoModel):

    def __init__(self, *args, **kwargs):
        super(PromotionCodeDao, self).__init__(*args, **kwargs)

    def update_one(self, filter: dict, obj: dict, extract=None, worker=False, *args, **kwargs):

        if extract is None:
            extract = {}

        obj['updated_time'] = dt_utcnow()

        if 'updated_by' not in obj:
            raise Exception('Required updated_by')
        if worker:
            self.worker(
                func='update_one',
                filter=filter,
                obj=obj,
                extract=extract,
                *args, **kwargs
            )
        else:
            return self.col.update_one(filter=filter, update={
                '$set': obj,
                **extract
            }, *args, **kwargs)
