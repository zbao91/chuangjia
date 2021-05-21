# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   basemodel
    Description: model 基类
    Author:      wzj
    Date:        2019/7/24
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

from peewee import *
from dbdriver import mdb


class BaseModel(Model):

    class Meta:
        database = mdb


