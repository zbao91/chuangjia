# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   partshare
    Description: 
    Author:      wzj
    Date:        2019-08-21
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import datetime
from models.basemodel import BaseModel
from peewee import *

class PartShareModel(BaseModel):
    """
    零件分享
    """
    class Meta:
        table_name = 'app_part_share_new'
    shareid = PrimaryKeyField()
    valid_time = DateTimeField()
    create_time = DateField(default=datetime.datetime.now)
    yc_id = CharField(max_length=32)
    pid = CharField(max_length=30)
    brandCode = CharField(max_length=20)
    port = CharField(max_length=10)
    mcid = CharField(max_length=300)

class AppPartShareLog(BaseModel):
    """
    分享日志
    """
    class Meta:
        table_name = 'app_part_share_log'
    shareid = IntegerField()
    createtime = DateField(default=datetime.datetime.now)
    ip = BigIntegerField(default=0)

