# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   redis
    Description: 
    Author:      wzj
    Date:        2019/7/23
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import time
import logging
import redis


class LinkedRedis(object):
    """
    常链接
    """
    max_idle_time = 3600 * 2

    def __init__(self, config_dict):
        self._config_dict = config_dict
        self.__db = None

    def _connect(self, config_dict):
        try:
            host, port, db, password = config_dict["host"], config_dict["port"], config_dict["db"], config_dict["password"]
            pool = redis.ConnectionPool(host=host, port=port, db=db, password=password, decode_responses=True)
            self.__db = redis.Redis(connection_pool=pool, decode_responses=True)
        except Exception:
            logging.error('mongo 链接失败')

    def get_instance(self):
        if self.__db is None:
            self._connect(self._config_dict)
        return self.__db

    # def __getattr__(self, item):
    #     if not self._db or self.max_idle_time < (int(time.time()) - self._last_use_time):
    #         self.__db.close()
    #         self._connect(self._config_dict)
    #     self._last_use_time = time.time()
    #     if not self.__db:
    #         return None
    #     return getattr(self.__db, item)

