# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   message
    Description: 
    Author:      bzq
    Date:        2021/04/12
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
import time
import ujson
import hashlib
import os
import uuid
import datetime

from utils.httpmixin import HTTPContent
from apps.handler import BaseHandler, UserBaseHandler
from config.config import SECRETE_KEY
from core.cache import *

class Login(UserBaseHandler):
    """
    登陆接口
    """
    login = False
    def post(self):
        result = {
            "code": 1,
            "msg":"成功",
            "time": int(time.time()),
            "data": None,
        }
        # 获取参数
        username = self._xss(self.get_argument("username", ""))
        password = self._xss(self.get_argument("password", ""))
        if not username or not password:
            result["code"] = 0
            result["msg"] = "请输入用户名或密码"
            self.write(result)
            self.finish()
            return
        # 获取该人员的数据
        keyList = ['password', 'salt', 'password', "role", "name"]
        condition = {
            "where" : [("username", username, "=", "and"),("status", '1', "=", "")],
        }
        sql = self._sql._select("user", keyList, **condition)
        data = self._mdb.get(sql)
        if not data:
            result["code"] = 0
            result["msg"] = "账号不存在，请确认后重新输入"
            self.write(result)
            self.finish()
            return
        check_password = data.get("password")
        salt = data.get("salt")
        role = data.get("role")
        name = data.get("name") if data.get("name") else "创佳用户"
        password += salt
        # 进行密码校验
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        if (check_password != hashed_password):
            result["code"] = 0
            result["msg"] = "密码错误，请确认后重新输入"
            self.write(result)
            self.finish()
            return
        # 保存设置用户token
        token = uuid.uuid4().hex
        set_to_redis("%s_token" % username, token, 7 * 24 * 3600)
        # 获取人员账号类型
        set_to_redis("%s_role" % username, role, 7 * 24 * 3600)
        result_dict = {
            "token": token,
            "role": role,
            "username": username,
            "name": name
        }
        result["data"] = result_dict
        self.write(result)
        self.finish()
        return

class Logout(UserBaseHandler):
    login = True
    def post(self):
        result = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None
        }
        # 获取参数
        username = self._xss(self.get_argument("username", ""))
        token = self._xss(self.get_argument("token", ""))
        if not username or not token:
            result["code"] = 0
            result["msg"] = "参数错误"
            self.write(result)
            self.finish()
            return
        # 获取token且校验
        rds_token = get_from_redis("%s_token" % username)
        if rds_token != token:
            result["code"] = 0
            result["msg"] = "token有误"
            self.write(result)
            self.finish()
            return
        delete_from_redis("%s_role" % username)
        delete_from_redis("%s_token" % username)
        self.write(result)
        self.finish()
        return

class ResetPassword(UserBaseHandler):
    login = True
    def post(self):
        result = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None
        }
        # 获取参数
        username = self._xss(self.get_argument("username", ""))
        old_password = self._xss(self.get_argument("old_password", ""))
        new_password1 = self._xss(self.get_argument("new_password1", ""))
        new_password2 = self._xss(self.get_argument("new_password2", ""))
        if not old_password:
            result["code"] = 0
            result["msg"] = "请输入旧密码"
            self.write(result)
            self.finish()
            return

        if not new_password1:
            result["code"] = 0
            result["msg"] = "请输入新密码"
            self.write(result)
            self.finish()
            return

        if not new_password2:
            result["code"] = 0
            result["msg"] = "请确认新密码"
            self.write(result)
            self.finish()
            return

        if new_password1 != new_password2:
            result["code"] = 0
            result["msg"] = "两次密码不一致"
            self.write(result)
            self.finish()
            return

        if not username:
            result["code"] = 0
            result["msg"] = "参数错误"
            self.write(result)
            self.finish()
            return

        # 获取该人员的数据
        valid_result, valid_msg = self.check_password(username, old_password)
        if not valid_result:
            result["code"] = 0
            result["msg"] = valid_msg
            self.write(result)
            self.finish()
            return
        condition = {
            "where": [("username", username, "=", "and"), ("status", '1', "=", "")],
        }
        hashed_password, salt = self.create_password(new_password1)
        update_dict = {
            "password": hashed_password,
            "salt": salt,
            "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        }
        sql = self._sql._update("user", update_dict, **condition)
        self._mwdb.execute(sql)
        delete_from_redis("%s_role" % username)
        delete_from_redis("%s_token" % username)
        self.write(result)
        self.finish()
        return

class CreateAccount(UserBaseHandler):
    """
    创建账号 - 管理员
    """
    login = True
    role = ["admin"]
    def post(self):
        result = {
            "code":1,
            "msg":"成功",
            "time": int(time.time()),
            "data" : []
        }
        name = self._xss(self.get_argument("name", ""))
        phone_number = self._xss(self.get_argument("phone_number", ""))
        department = self._xss(self.get_argument("department", ""))
        position = self._xss(self.get_argument("position", ""))
        role = self._xss(self.get_argument("role", ""))
        if not name or not phone_number or not role:
            result["code"] = 0
            result["msg"] = "必填字段缺失"
            self.write(result)
            self.finish()
            return
        condition = {
            "where": [("username", phone_number, "=", "and"), ("status", '1', "=", "")],
        }
        keyList = ["*"]
        sql = self._sql._select("user", keyList, **condition)
        check_res = self._mdb.get(sql)
        if check_res:
            result["code"] = 0
            result["msg"] = "该手机已被使用"
            self.write(result)
            self.finish()
            return
        hashed_password, salt = self.create_password("aa123456")
        insert_dict = {
            "name": name,
            "username": phone_number,
            "password": hashed_password,
            "salt": salt,
            "create_time": datetime.datetime.today(),
            "department": department,
            "role": role,
            "position": position,
        }
        sql = self._sql._insert("user", insert_dict)
        self._mdb.execute(sql)
        self.write(result)
        self.finish()
        return

class AccountList(UserBaseHandler):
    """
    账号列表 - 管理员
    """
    login = False
    # role = ["admin"]
    role = None
    def get(self):
        page = self._xss(self.get_argument("page_number", "1"))
        print(page)
        response = {
            "code":1,
            "msg":"成功",
            "time": int(time.time()),
            "data" : []
        }
        condition = {
            "where": [("status", '1', "=", "")],
        }
        keyList = ["count(1) as counter"]
        sql = self._sql._select("user", keyList, **condition)
        total_elements = self._mdb.get(sql).get("counter")

        start, end = self.pagination(page)
        # 获取数据
        condition = {
            "where": [("status", '1', "=", "")],
            "limit": [start, end],
            "order": " id asc"
        }
        keyList = ["id", "name", "username", "department", "role"]
        sql = self._sql._select("user", keyList, **condition)
        print(sql)
        res = self._mdb.query(sql)
        result_dict = {
            "content": res,
            "total_elements": total_elements,
        }
        response["data"] = result_dict
        self.write(response)
        self.finish()
        return

class RestPasswordDefault(UserBaseHandler):
    """
    重置用户密码至默认 - 管理员
    """
    login = False
    # role = ["admin"]
    role = None
    def post(self):
        uid = self._xss(self.get_argument("uid", "1"))
        response = {
            "code":1,
            "msg":"成功",
            "time": int(time.time()),
            "data" : []
        }

        condition = {
            "where": [("id", uid, "=", "")]
        }
        keyList = ["*"]
        sql = self._sql._select("user", keyList, **condition)
        user_info = self._mdb.get(sql)
        if not user_info:
            response["code"] = 0
            response["msg"] = "该用户不存在"

        hashed_password, salt = self.create_password("aa123456")
        update_dict = {
            "password": hashed_password,
            "salt": salt,
            "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        }
        sql = self._sql._update("user", update_dict, **condition)
        self._mwdb.execute(sql)
        self.write(response)
        self.finish()
        return

class DeleteAccount(UserBaseHandler):
    """
    删除账号 - 管理员
    """
    login = False
    # role = ["admin"]
    role = None
    def post(self):
        uid = self._xss(self.get_argument("uid", "1"))
        response = {
            "code":1,
            "msg":"成功",
            "time": int(time.time()),
            "data" : []
        }

        condition = {
            "where": [("id", uid, "=", "")]
        }
        keyList = ["*"]
        sql = self._sql._select("user", keyList, **condition)
        user_info = self._mdb.get(sql)
        if not user_info:
            response["code"] = 0
            response["msg"] = "该用户不存在"

        update_dict = {
            "status": -1,
            "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        }
        sql = self._sql._update("user", update_dict, **condition)
        self._mwdb.execute(sql)
        self.write(response)
        self.finish()
        return

class AccountInfo(UserBaseHandler):
    """
    账号信息 - 管理员
    """
    login = False
    # role = ["admin"]
    role = None
    def get(self):
        uid = self._xss(self.get_argument("uid", "0"))
        response = {
            "code":1,
            "msg":"成功",
            "time": int(time.time()),
            "data" : []
        }

        condition = {
            "where": [("id", uid, "=", "")]
        }
        keyList = ["*"]
        sql = self._sql._select("user", keyList, **condition)
        user_info = self._mdb.get(sql)
        if not user_info:
            response["code"] = 0
            response["msg"] = "该用户不存在"

        response["data"] = user_info
        self.write(response)
        self.finish()
        return

class EditAccount(UserBaseHandler):
    """
    编辑账号信息
    """
    login = False
    # role = ["admin"]
    role = None
    def post(self):
        uid = self._xss(self.get_argument("uid", "0"))
        name = self._xss(self.get_argument("name", ""))
        phone_number = self._xss(self.get_argument("phone_number", ""))
        department = self._xss(self.get_argument("department", ""))
        position = self._xss(self.get_argument("position", ""))
        role = self._xss(self.get_argument("role", ""))
        response = {
            "code":1,
            "msg":"成功",
            "time": int(time.time()),
            "data" : []
        }

        if not name or not phone_number or not role:
            response["code"] = 0
            response["msg"] = "必填字段缺失"
            self.write(response)
            self.finish()
            return
        condition = {
            "where": [("username", phone_number, "=", "and"), ("id", uid, "!=", "and"), ("status", '1', "=", "")],
        }
        keyList = ["*"]
        sql = self._sql._select("user", keyList, **condition)
        check_res = self._mdb.get(sql)
        if check_res:
            response["code"] = 0
            response["msg"] = "该手机已被使用"
            self.write(response)
            self.finish()
            return

        condition = {
            "where": [("id", uid, "=", "")]
        }
        keyList = ["*"]
        sql = self._sql._select("user", keyList, **condition)
        user_info = self._mdb.get(sql)
        if not user_info:
            response["code"] = 0
            response["msg"] = "该用户不存在"

        update_dict = {
            "name": name,
            "username": phone_number,
            "department": department,
            "role": role,
            "position": position,
            "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        }
        sql = self._sql._update("user", update_dict, **condition)
        self._mdb.execute(sql)
        response["data"] = user_info
        self.write(response)
        self.finish()
        return

class CreateAccountTmp(BaseHandler):
    """
    创建账号
    """
    login = False

    def post(self):
        result = {
            "code":1,
            "msg":"成功",
            "time": int(time.time()),
            "data" : []
        }
        username = self._xss(self.get_argument("username", ""))
        password = self._xss(self.get_argument("password", ""))
        salt = uuid.uuid4().hex
        password += salt
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        insert_dict = {
            "username": username,
            "password": hashed_password,
            "salt": salt,
            "create_time": datetime.datetime.today()
        }
        sql = self._sql._insert("user", insert_dict)
        self._mdb.execute(sql)
        self.write(result)
        self.finish()
        return
