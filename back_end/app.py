# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   app
    Description: 
    Author:      wzj
    Date:        2019/7/23
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import utils.logging

import logging
from tornado import httpserver, ioloop
from tornado.options import define, options

from core.application import BaseApplication

from apps import urls


define("port", default=9023, type=int)
options.parse_command_line()

def make_app():
    server = httpserver.HTTPServer(BaseApplication(urls, port=options.port))
    return server

def main():
    server = make_app()
    server.listen(options.port, address="0.0.0.0")
    print("start success,the port is [%d]" % options.port)
    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
