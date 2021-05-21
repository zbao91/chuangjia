# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   role
    Description: 
    Author:      wzj
    Date:        2019/8/3
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import datetime
from peewee import *

from ..basemodel import BaseModel

class UserRoleModel(BaseModel):

    class Meta:
        table_name = 'user_role'

    yc_id = CharField(max_length=32, verbose_name='用户ID')
    brandCode = CharField(max_length=20, verbose_name='品牌:对应品牌表中 brandcode对应的code字段')
    valid_datetime = DateTimeField(verbose_name='有效日期(精确到秒)')
    access_type = CharField(max_length=40, default='brand')
    create_time = DateTimeField()
    update_time = DateTimeField()
    status = SmallIntegerField(default=1, verbose_name='1激活 0失效')
