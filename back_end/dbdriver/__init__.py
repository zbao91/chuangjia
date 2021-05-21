# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   __init__.py
    Description: 
    Author:      wzj
    Date:        2019/7/23
-------------------------------------------------
    Change Activity:
    新的服务使用了 peewee orm
    部分接口没有重写，为兼容之前的torndb方式查询db的代码,这里有两个mysql的连接，后期请合并，并且使用连接池

-------------------------------------------------
"""


from config.redis import rds
from config.mysql import mdb_read

from .redis import LinkedRedis
from .mysql import ReConnectMysqlDatabase
from .sql import  SqlHandlers
from .tordb import Connection

rdb = LinkedRedis(rds).get_instance()



tdb = Connection(mdb_read['host'], mdb_read['database'], mdb_read['user'], mdb_read['password'])
database = mdb_read.pop('database')
mdb_read.pop('db', '')
mdb = ReConnectMysqlDatabase(database, **mdb_read)
sql_format = SqlHandlers()
