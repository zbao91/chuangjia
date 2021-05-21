# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   valid
    Description: 
    Author:      wzj
    Date:        2019/8/4
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import time
import logging

from config.config import APPKEY
from core.func import calculate_md5
from core.errors import BadArgError, LoginNeedException, LoginTokenException
from dbdriver import rdb
from core.role import vin_brandCode_default

from core.cache import lru_cache

ROLE_LOGIN = 8
ROLE_VIN = 16
ROLE_EPC = 4
ROLE_MAIN = 2
ROLE_ARTICLE = 1
ROLE_PART = 32

ALL_ROLE = {ROLE_ARTICLE, ROLE_MAIN, ROLE_EPC, ROLE_VIN}


class UserValid(object):
    """
    用户校验
    """
    param_timeout = 180

    def __init__(self):
        pass

    def set_params(self, params:dict):
        self.params = params

    def get_argument(self, argument, default=''):
        return self.params.get(argument, default)


    def _check_args(self):
        """
        功能: 检查接口是否有效，防止机器模拟请求
        描述:
            1. 检查请求时间是否有效；
            2. 校验客户端加密hash是否正确
        """
        params = self.params
        # 检查请求时间是否有效
        if time.time() - int(params.get('time', 0)):
            raise BadArgError('参数异常')
        device = params.get('device')
        if device != 'h5':
            # 校验客户端加密hash是否正确
            keys = sorted(list(params.keys()))
            sign = "" # 参数值累加加密
            for key in keys:
                if key == "hash":
                    continue
                sign += params[key][0].decode('utf-8')
            if not sign:
                raise LoginTokenException('登录异常')
            sign += APPKEY
            if calculate_md5(sign) != params.get('hash', ''):
                raise BadArgError('参数校验异常')
        return True

    def _check_login(self):
        """
        校验登录
        :return:
        """
        username = self.request.headers.get("user")
        hashid = self.request.headers.get('token', '')
        if rdb.get("%s_token" % username) != hashid:
            raise LoginNeedException('请重新登录')
        return username

    def check_share(self):
        """
        零件分享入口
        :return:
        """
        # 该字段表示接口为分享接口, 且分享有效
        if 'shareid' in self.params:
            return self.role.check_share_role(self.params['shareid'])
        else:
            return True

    @lru_cache(300, 180)
    def check_use_role(self, yc_id, brandCode, role):
        if role == ROLE_EPC:
            return self.check_epc_role(yc_id, brandCode)
        elif role == ROLE_ARTICLE:
            return self.check_article_role(yc_id)
        elif role == ROLE_MAIN:
            return self.check_maintance_role(yc_id)
        elif role == ROLE_VIN:
            return self.check_vin_role(yc_id, brandCode)
        elif role == ROLE_PART:
            return self.check_part_role(yc_id)
        else:
            return False

    def check_use_role_no_cache(self, yc_id, brandCode, role):
        if role == ROLE_EPC:
            return self.check_epc_role(yc_id, brandCode)
        elif role == ROLE_ARTICLE:
            return self.check_article_role(yc_id)
        elif role == ROLE_MAIN:
            return self.check_maintance_role(yc_id)
        elif role == ROLE_VIN:
            return self.check_vin_role(yc_id, brandCode)
        else:
            return False

    def check_epc_role(self, yc_id, brandCode):
        # 普通epc接口
        return self.role.check_user_epc_role(yc_id=yc_id, brandCode=brandCode)

    def check_maintance_role(self, yc_id):
        # 维修保养件
        return self.role.check_user_maintenance_role(yc_id)

    def check_vin_role(self, yc_id, brandCode):
        return self.role.check_user_vin_role(yc_id, brandCode)

    def check_article_role(self, yc_id):
        # 品牌件
        return self.role.check_article_role(yc_id)

    def check_login(self):
        return self._check_login()

    def check_part_role(self, yc_id):
        return self.role.check_user_epc_role(yc_id, vin_brandCode_default)
