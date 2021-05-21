# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   application
    Description: 
    Author:      wzj
    Date:        2019/7/23
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import ujson
import logging
import os

from tornado.web import Application, URLSpec

from config.config import DEBUG



class BaseApplication(Application):
    def __init__(self, handlers=None, default_host=None, transforms=None, **settings):
        setting = {
            'debug': DEBUG,
            'log_function': log_request,
            "static_path": os.path.join(os.getcwd(), "files"),
            "static_url_prefix": "/resources",
        }
        print(setting)

        setting.update(settings)
        self.port = settings.pop('port', 0)
        super().__init__(handlers, default_host, transforms, **setting)


def log_request(handler):
    if handler.get_status() != 200:
        logging.error(handler.request.arguments)
    template = '[{port}][{http_code:>4}]:[{method:>4}]:[{path}]::[uid:{uid}]:[{time:0.2f}ms]:[{code}]:[{msg}]--[{arg}]'
    data = {
        'port': handler.application.port,
        'http_code': handler.get_status(),
        'time': 1000.0 * handler.request.request_time(),
        'path': handler.request.uri,
        'method': handler.request.method,
        'uid': handler.get_argument('uid', ''),
        'code': getattr(handler, 'return_code', -100),
        'msg': getattr(handler, 'return_msg', '无提示'),
        'arg': getattr(handler,'log_args', '')
    }
    logging.error(template.format(**data))


class MyPrefixURLSpec(URLSpec):
    def __init__(self, pattern, handler, kwargs=None, name=None):
        self.pre_pattern = pattern
        self.pre_name = name
        self.pre_kwargs = kwargs
        self.pre_handler = handler
        super().__init__(pattern, handler, kwargs, name)


url = MyPrefixURLSpec


