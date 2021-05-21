# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   httpmixin
    Description: 远端http请求
    Author:      wzj
    Date:        2019/7/24
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import logging

from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError
from tornado.httputil import url_concat, urlencode
from tornado.escape import json_decode

from core.errors import BaseRPCError, BaseError


class GetHTTPRequest(HTTPRequest):
    """
    praam: 查询参数 字典对象
    """
    def __init__(self, url, param=None, **kwargs):
        if param:
            url = url_concat(url, param)
        super().__init__(url, "GET", **kwargs)

class PostHTTPRequest(HTTPRequest):
    """
    仅支持简单的application/x-www-form-urlencoded类型的post请求
    data: None or dict
    """
    def __init__(self, url, data=None, param=None, **kwargs):
        body = data or {}
        body.update(kwargs.pop('body', {}))
        if param:
            url = url_concat(url, param)
        super().__init__(url, 'POST', body=urlencode(body), **kwargs)


class HTTPContent(object):
    """远程http请求

    如果发生异常，get/post会直接raise
    """
    host = ''

    @classmethod
    def check_callback(self, callback):
        if callback and not callable(callback):
            raise NotImplementedError
            # raise NError(str(callback)+'必须为可调用对象')


    @classmethod
    async def get(cls, uri:str, param=None, arg_rename=None, **kwargs):
        if not uri.startswith('http'):
            if not cls.host:
                raise NotImplementedError
            url = cls.host + uri
        else:
            url = uri
        param = {} if param is None else param
        param.update(kwargs)
        if arg_rename:
            for arg, narg in arg_rename.items():
                if arg in param:
                    param[narg] = param.pop(arg)
        request = GetHTTPRequest(url, param)
        return await cls.send_request(request)

    @classmethod
    async def post(cls, uri, data=None, param=None, arg_rename=None, **kwargs):
        if not uri.startswith('http'):
            if not cls.host:
                raise NotImplementedError
            url = cls.host + uri
        else:
            url = uri
        data = {} if data is None else data
        data.update(kwargs)
        if arg_rename:
            for arg, narg in arg_rename.items():
                if arg in data:
                    data[narg] = data.pop(arg)
        request = PostHTTPRequest(url, data=data, param=param)
        return await cls.send_request(request)

    @classmethod
    async def send_request(self, request):
        try:
            response = await AsyncHTTPClient().fetch(request)
            rjson = json_decode(response.body)
        except (HTTPError, ValueError) as e:
            raise BaseRPCError
        else:
            return rjson


