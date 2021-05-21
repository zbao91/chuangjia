# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   __init__.py
    Description: 
    Author:      wzj
    Date:        2019/7/23
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import tornado.web
import os

from .user import user_url
from .files import files_url
from .standard_management import standard_url
from .image_management import image_url

path = os.path.join(os.getcwd(), "files")
urls = [
    (r'/download/(.*)',tornado.web.StaticFileHandler,{'path':path}),
]

urls.extend(user_url)
urls.extend(files_url)
urls.extend(standard_url)
urls.extend(image_url)



