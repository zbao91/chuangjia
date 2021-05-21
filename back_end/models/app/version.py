# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   version
    Description: 
    Author:      wzj
    Date:        2019-08-22
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

from peewee import *
from models.basemodel import BaseModel

class VersionModel(BaseModel):

    class Meta:
        table_name = 'app_version'

    platform = CharField(max_length=20)
    force_update = SmallIntegerField(default=0)
    update_time = DateField()
    version = CharField(max_length=10)
    status = SmallIntegerField(default=1)
    download_url_3_party = CharField(max_length=100, default='')
    md5_verify = CharField(max_length=40, default='')
    msg = CharField(max_length=300, default='')