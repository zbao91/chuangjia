# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   profile
    Description: 
    Author:      wzj
    Date:        2019-08-21
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
from peewee import *

from models.basemodel import BaseModel


class SimpleUserProfileModel(BaseModel):
    """用户信息"""
    class Meta:
        table_name = 'user_profile'

    yc_id = CharField(max_length=32)
    username = CharField(max_length=60)
    full_name = CharField(max_length=40)
    phone = CharField(max_length=20)
    company = CharField(max_length=50)

    logo_url = CharField(max_length=100)
    usc_url = CharField(max_length=100)
    avatar = CharField(max_length=100)
