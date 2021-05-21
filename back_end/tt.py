# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   tt
    Description: 
    Author:      wzj
    Date:        2019-11-01
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""
# -*- coding: utf-8 -*-
# @Time    : 2019/08/20 下午1:54
# @Author  : Sean
# @Site    : beacon_business
# @Software: PyCharm

import time
import datetime
import json
import bcrypt
import logging

from config.cache_key import USERINFO_KEY
from base.base import BaseModel
from management.companyModel import Company


class AuthModel(BaseModel):
    """
    用户
    """

    def __init__(self, handler_mod):
        """"""
        super(AuthModel, self).__init__(handler_mod)

    def login(self, username, password):
        """
        登录验证
        :param username: 登录名/账号
        :param password: 密码
        :return:
        """
        userinfo = None
        message = ""

        query_list = ['uid', 'username', 'encrypt_pwd', 'status', "company_id", "user_type"]
        condition = {
            'where': [('username', username, '=', '')],
            'limit': (0, 1),
        }
        sql_str = self._sql._select("beacon_user", query_list, **condition)
        user = self._mdb["business"].fetchone(sql_str)

        encrypt_pwd = bcrypt.hashpw(password.encode("utf-8"), user['encrypt_pwd'].encode("utf-8")) if user else ""
        if not user:
            message = "没有这个用户"
        elif user["status"] != 1:
            message = "该账号异常，请联系客服协助处理"
        elif password and encrypt_pwd and (str(encrypt_pwd, encoding="utf-8") == user['encrypt_pwd']):
            userinfo = user
            # 验证成功
            self.flushLoginTime(user["uid"])
        else:
            message = "账号或密码不正确"
        return userinfo, message

    def creatLoginUser(self, user_info, auto=False):
        """
        创建登录用户
        :param user_info: {
            "username": 手机/email, 登录名
            "full_name": 全名,
            "pwd" : 密码,
            "phone": 手机号
            "email": email,
            "reg_type": phone/email, # 注册类型，手机注册/邮箱注册
            "country_code": "+86"   # 手机号国家代码 , 默认中国
        }
        :param auto: 是否是系统自动创建的, 部分情况是系统自动创建，需要标志出来
        :return: user_info = {
            "uid": "xxxxx",
            ...
        }, message
        """
        userinfo = None
        message = ""
        username = user_info.get("username")
        reg_type = user_info.get("reg_type", "phone")
        avatar = user_info.get("avatar", "")
        user_type = user_info.get("user_type", "master")
        company_id = user_info.get("company_id", "")
        channel = user_info.get("channel", "mgmt_sys")
        email = user_info.get("email", "")
        phone = user_info.get("phone", "")  # 优先使用u_dic传递过来的phone，若为空，则使用username
        role_id = user_info.get("role_id", 0)
        registe_code = user_info.get("code", "")  # 注册代号，默认空，用来标记特殊活动过注册的用户
        user_extis = self.checkUsername(username)
        if user_extis:
            message = "已存在该用户"
        else:
            # 如果注册方式为手机注册
            if reg_type == 'phone':
                if not phone:
                    phone = username
            else:
                if not email:
                    email = username

            full_name = user_info.get("full_name", username)
            # 没有密码，使用登录名后6位
            registeTime = time.strftime("%Y-%m-%d %X", time.localtime())
            pwd = str(user_info["pwd"]) if user_info.get("pwd", None) else str(username[-6:])
            hashed_pass = bcrypt.hashpw(pwd.encode(encoding="utf-8"), bcrypt.gensalt(8))
            uid = self.getMd5(username + registeTime)

            # 用户账号信息
            user = {
                "uid": uid,
                "username": username,
                "encrypt_pwd": str(hashed_pass, encoding="utf-8"),
                "register_datetime": registeTime,
                "company_id": company_id,
                "channel": channel,
                "user_type": user_type,
                "status": 1
            }

            sql_u = self._sql._insert("beacon_user", user)
            self._mdb["business"].execute(sql_u)

            # 保存用户拓展信息
            profileDict = {
                "uid": uid,
                "phone": phone,
                "email": email,
                "avatar": avatar,
                "role_id": role_id,
                "preferredlanguage": "zh-cn",
                "wechat_bind": 0,
                "wecaht_name": "",
                "full_name": full_name,
            }

            sql_u = self._sql._insert("beacon_user_profile", profileDict)
            row_counts = self._mdb["business"].execute(sql_u)
            logging.info('success: insert%s one record!' % row_counts)
            userinfo = profileDict
        return userinfo, message

    def checkUsername(self, username, query_list=None, status="normal"):
        """
        校验用户是否存在
        :param username:  "xxxxx"
        :param query_list: [ , , ]
        :param status: 默认normal
        :return: user
        """
        if not query_list:
            query_list = ["username", "phone", "email", "status"]
        condition = {
            "where": [("username", username, "=", "and"), ("status", status, "=", "")],
            "limit": (0, 1)
        }
        u_sql = self._sql._select("beacon_user", query_list, **condition)
        user_inf = self._mdb["business"].fetchone(u_sql)
        return user_inf

    def checkSmsCode(self, phone, sms_code, sms_type):
        """
        检查验证码是否正确
        :param phone:
        :param sms_code:
        :param sms_type: login/register/bind/drawal
        :return:
        """
        checked, msg = True, ''

        redis_sms = self._rsdb["business"].get('%s_code_%s' % (sms_type, phone))
        if not redis_sms:
            checked = False
            msg = '未点击发送验证码或验证码已过期'
            return checked, msg

        sms_info = json.loads(redis_sms.decode('utf-8'))
        logging.info(sms_info)
        if sms_code != sms_info.get('sms_code'):
            checked = False
            msg = '验证码不正确'
            return checked, msg
        return checked, msg

    def closeUser(self, user_id):
        """
        封禁用户
        :param user_id:
        :return:
        """
        condition = {
            'where': [('uid', user_id, '=', '')]
        }

        u_sql = self._sql._update('beacon_user', keyDict={"status": 0}, **condition)
        self._mdb["business"].execute(u_sql)
        return True

    def queryUserBaseInfo(self, uid, query_list=None):
        """
        查询用户总表的基础信息
        :param uid: 用户的ID
        :return: user_info
        """
        if query_list is None:
            query_list = ["company_id", "username", "user_type", "status", "uid"]

        condition = {
            "where": [("uid", uid, "=", "")],
            "limit": (0, 1)
        }
        u_sql = self._sql._select("beacon_user", query_list, **condition)
        user_info = self._mdb["business"].fetchone(u_sql)
        return user_info

    def query_user_profile(self, uid, query_list=None):
        """
        查询用户总表的基础信息
        :param uid: 用户的ID
        :return: user_info
        """
        if query_list is None:
            query_list = ["full_name", "phone", "avatar", "last_login", "role_id"]

        condition = {
            "where": [("uid", uid, "=", "")],
            "limit": (0, 1)
        }
        u_sql = self._sql._select("beacon_user_profile", query_list, **condition)
        user_info = self._mdb["business"].fetchone(u_sql)
        return user_info

    def update_user_profile(self, uid, edit_args):
        """
        更新用户拓展信息
        :param uid: 用户ID
        :param edit_args: 修改的内容
        :return:
        """
        condition = {
            "where": [("uid", uid, "=", "")]
        }
        u_sql = self._sql._update('beacon_user_profile', keyDict=edit_args, **condition)
        rows = self._mdb["business"].execute(u_sql)
        return rows

    def flushLoginTime(self, user_id, login_time=None):
        """
        更新用户最后登录时间
        :param uid: user_id
        :param login_time: datetime.datetime obj
        :return:
        """
        if not login_time:
            login_time = datetime.datetime.now()
        condition = {
            "where": [("uid", user_id, "=", "")],
        }
        upd_sql = self._sql._update("beacon_user_profile", {"last_login": login_time.strftime("%Y-%m-%d %H:%M:%S")}, **condition)
        self._mdb["business"].execute(upd_sql)

    def cache_user_base_info(self, userinfo, expires_time=None):
        """
        缓存 用户基础信息
        :param userinfo:
        :param expires_time: 缓存有效期 单位：秒
        :return:
        """
        if not expires_time:
            expires_time = 60 * 60 * 24
        user_info_key = "%s_%s" % (USERINFO_KEY, userinfo["uid"])
        self._rsdb["business"].set(user_info_key, json.dumps(userinfo))
        self._rsdb["business"].expire(user_info_key, expires_time)
        return userinfo

    def get_user_cache_info(self, user_id):
        """
        获取用户缓存信息，没有缓存 会自动加载
        :param user_id: 用户uid
        :return:
        """
        user_info_key = "%s_%s" % (USERINFO_KEY, user_id)
        cache_info = self._rsdb["business"].get(user_info_key)
        if cache_info:
            cache_info = json.loads(cache_info)
        else:
            user_info = self.get_user_base_info(user_id)
            cache_info = self.cache_user_base_info(user_info)
        return cache_info

    def get_user_base_info(self, user_id):
        """
        查询用户基础信息(个人，加公司 基础信息)
        :param user_id: 用户 uid
        :return:
        """
        base_info = self.queryUserBaseInfo(user_id)
        profile_info = self.query_user_profile(user_id)
        company_id = base_info.pop("company_id", None)
        if base_info and company_id:
            company_obj = Company(self)
            company_info = company_obj.queryCompany({"uuid": company_id}, keyList=["company_name", "uuid"])
            profile_info["company"] = company_info[0]

        base_info.update(profile_info)
        base_info["last_login"] = datetime.datetime.strftime(base_info["last_login"], "%Y-%m-%d %H:%M:%S")
        return base_info








































# -*- coding: utf-8 -*-
# @Time    : 2019-08-25 22:14
# @Author  : Sean
# @Site    : beacon_business
# @Software: PyCharm

import time
import datetime
import logging
import traceback
from copy import deepcopy

from base.base import BaseModel


COMPANY_STATUS_DIC = {"active": 1, "closed": 0, "warning": -1, "comfirming": -2}


class Company(BaseModel):
    """
    公司
    """

    def __init__(self, handler_mod):
        """"""
        super(Company, self).__init__(handler_mod)

    def createCompany(self, company_info):
        """
        创建一个公司
        :param company_info: {
            "company_name": "公司名称",
            "shortname": "公司简称"
            "contacts_people": "联系人姓名",
            "legal_person": "法人",
            "phone": "13xxxxx",  # 商户联系人手机
            "tel": "0571-xxxx",     # 商户联系电话
            "company_type": "manufactures" manufactures: 厂商(品牌方), dealer: 经销商, retailer: 零售商,
            "comment": "商户说明",
            "account_id": "", 系统账号id
            "status": "closed",    active: 正常，closed: 封停, warning: 账户异常, comfirming: 审核中
        }
        :return:
        """
        success = True
        back_info = None
        # 参数校验
        exist_info = [(key in company_info) for key in ["company_name", "contacts_people", "phone"]]
        if not all(exist_info):
            success = False
            back_info = "参数不足"

        status = company_info.get("status", "active")

        id_str = company_info["company_name"] + company_info["phone"] + str(time.time())
        company_id = self.getMd5(id_str)
        beacon_company = {
            "uuid": company_id,
            "company_name": company_info.get("company_name", ""),
            "shortname": company_info.get("shortname", ""),
            "contacts_people": company_info.get("contacts_people", ""),
            "legal_person": company_info.get("legal_person", ""),
            "phone": company_info.get("phone", ""),
            "tel": company_info.get("tel", ""),
            "company_type": company_info.get("company_type", "manufactures"),
            "comment": company_info.get("comment", ""),
            "account_id": company_info.get("account_id", ""),
            "status": COMPANY_STATUS_DIC.get(status, 1),
            "createtime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        sql_i = self._sql._insert("beacon_company", beacon_company)

        try:
            created = self._mdb["business"].execute(sql_i)
            back_info = beacon_company
        except BaseException:
            logging.error("--------Error: %s" % traceback.format_exc())
            created = False

        if not created:
            success = False

        return (success, back_info)

    def upgradeCompany(self, company_uid, upd_info):
        """
        更新商家信息
        :param company_uid: 公司uid
        :param upd_info: 修改内容
        :return:
        """
        success = True
        if "status" in upd_info:
            upd_info["status"] = COMPANY_STATUS_DIC.get(upd_info["status"], -1)

        condition = {
            "where": [("uuid", company_uid, "=", "")],
        }
        sql_u = self._sql._update("beacon_company", upd_info, **condition)
        try:
            self._mdb["business"].execute(sql_u)
        except BaseException:
            logging.error("--------Error: %s" % traceback.format_exc())
            success = False
        return success, company_uid

    def queryCompanyCounts(self, filter_arg):
        """
        查询商户列表 数量
        :param filter_args: {
            "query": 模糊查询,
            "page": 页码,
            "per_page": 每页条数
            "status": active: 正常，closed: 封停, warning: 账户异常
        }
        :return:
        """
        page_info = {}
        filter_args = deepcopy(filter_arg)
        page = filter_args.pop("page", 0)
        per_page = filter_args.pop("per_page", 1)

        where_list = []
        query_str = filter_args.pop("query", None)
        status = filter_args.pop("status", None)

        for cl_key, value in filter_args.items():
            if value is not None:
                where_list.append((cl_key, value, "=", "and"))
        if query_str:
            sub_filter = [
                ("company_name", query_str, "like", "or"),
                ("phone", query_str, "like", "or"),
                ("email", query_str, "like", "or"),
                ("contacts_people", query_str, "like", "")
            ]
            where_list.append(("query_str", sub_filter, "sub", "and"))

        if status not in [None, ""]:
            where_list.append(("status", COMPANY_STATUS_DIC.get(status, 1), "=", ""))
        else:
            where_list.append(("status", "-3", "!=", ""))
        condition = {
            "where": where_list,
        }

        count_sql = self._sql._select("beacon_company", ["uuid) AS counts"], **condition)
        count_info = self._mdb["business"].fetchone(count_sql)
        total = count_info["counts"]
        if total:
            page_info = {
                "total": total,
                "total_page": int(total / per_page) + 1 if total % per_page else int(total / per_page)
            }
        return page_info

    def queryCompany(self, filter_arg, keyList=None, order_by=None):
        """
        查询商户列表
        :param filter_args: {
            "query": 模糊查询,
            "page": 页码,
            "per_page": 每页条数
            "uuid": 公司id,
            "company_uid_list": 商户id列表
            "status": active: 正常，closed: 封停, warning: 账户异常
            "createtime": 创建时间
        }
        :return:
        """
        if not keyList:
            keyList = ["uuid", "company_name", "phone", "contacts_people", "email", "status", "address"]
        filter_args = deepcopy(filter_arg)
        page = filter_args.pop("page", 0)
        per_page = filter_args.pop("per_page", 1)
        where_list = []
        query_str = filter_args.pop("query", None)
        status = filter_args.pop("status", None)
        company_uid_list = filter_args.pop("company_uid_list", None)
        for cl_key, value in filter_args.items():
            if value is not None:
                where_list.append((cl_key, value, "=", "and"))
        if query_str:
            sub_filter = [
                ("company_name", query_str, "like", "or"),
                ("phone", query_str, "like", "or"),
                ("email", query_str, "like", "or"),
                ("contacts_people", query_str, "like", "")
            ]
            where_list.append(("query_str", sub_filter, "sub", "and"))

        if company_uid_list:
            if len(company_uid_list) > 1:
                where_list.append(("uuid", tuple(company_uid_list), "in", "and"))
            else:
                where_list.append(("uuid", company_uid_list[0], "=", "and"))

        if status not in [None, ""]:
            where_list.append(("status", COMPANY_STATUS_DIC.get(status, 1), "=", ""))

        if not order_by:
            order_by = [("createtime", "DESC")]
        condition = {
            "where": where_list,
            "order": order_by
        }
        if page:
            limit_start = (page - 1) * per_page
            condition["limit"] = (limit_start, per_page)
        query_sql = self._sql._select("beacon_company", keyList, **condition)
        company_info = self._mdb["business"].fetchmany(query_sql)

        return company_info

    # ------------------------------- tools ------------------------------

    def checkCompanyName(self, company_name, query_list=None):
        """
        校验用户是否存在
        :param username:  "xxxxx"
        query_list: [ , , ]
        :return: user
        """
        if not query_list:
            query_list = ["company_name", "phone", "contacts_people", "status", "confirm_status"]
        condition = {
            "where": [("company_name", company_name, "=", "")],
            "limit": (0, 1)
        }
        u_sql = self._sql._select("beacon_company", query_list, **condition)
        company_inf = self._mdb["business"].fetchone(u_sql)
        return company_inf

















# -*- coding: utf-8 -*-
# @Time    : 2019-08-25 22:14
# @Author  : Sean
# @Site    : beacon_business
# @Software: PyCharm

import time
import datetime
import logging
import traceback
from copy import deepcopy

from base.base import BaseModel


COMPANY_STATUS_DIC = {"active": 1, "closed": 0, "warning": -1, "comfirming": -2}


class Company(BaseModel):
    """
    公司
    """

    def __init__(self, handler_mod):
        """"""
        super(Company, self).__init__(handler_mod)

    def createCompany(self, company_info):
        """
        创建一个公司
        :param company_info: {
            "company_name": "公司名称",
            "shortname": "公司简称"
            "contacts_people": "联系人姓名",
            "legal_person": "法人",
            "phone": "13xxxxx",  # 商户联系人手机
            "tel": "0571-xxxx",     # 商户联系电话
            "company_type": "manufactures" manufactures: 厂商(品牌方), dealer: 经销商, retailer: 零售商,
            "comment": "商户说明",
            "account_id": "", 系统账号id
            "status": "closed",    active: 正常，closed: 封停, warning: 账户异常, comfirming: 审核中
        }
        :return:
        """
        success = True
        back_info = None
        # 参数校验
        exist_info = [(key in company_info) for key in ["company_name", "contacts_people", "phone"]]
        if not all(exist_info):
            success = False
            back_info = "参数不足"

        status = company_info.get("status", "active")

        id_str = company_info["company_name"] + company_info["phone"] + str(time.time())
        company_id = self.getMd5(id_str)
        beacon_company = {
            "uuid": company_id,
            "company_name": company_info.get("company_name", ""),
            "shortname": company_info.get("shortname", ""),
            "contacts_people": company_info.get("contacts_people", ""),
            "legal_person": company_info.get("legal_person", ""),
            "phone": company_info.get("phone", ""),
            "tel": company_info.get("tel", ""),
            "company_type": company_info.get("company_type", "manufactures"),
            "comment": company_info.get("comment", ""),
            "account_id": company_info.get("account_id", ""),
            "status": COMPANY_STATUS_DIC.get(status, 1),
            "createtime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        sql_i = self._sql._insert("beacon_company", beacon_company)

        try:
            created = self._mdb["business"].execute(sql_i)
            back_info = beacon_company
        except BaseException:
            logging.error("--------Error: %s" % traceback.format_exc())
            created = False

        if not created:
            success = False

        return (success, back_info)

    def upgradeCompany(self, company_uid, upd_info):
        """
        更新商家信息
        :param company_uid: 公司uid
        :param upd_info: 修改内容
        :return:
        """
        success = True
        if "status" in upd_info:
            upd_info["status"] = COMPANY_STATUS_DIC.get(upd_info["status"], -1)

        condition = {
            "where": [("uuid", company_uid, "=", "")],
        }
        sql_u = self._sql._update("beacon_company", upd_info, **condition)
        try:
            self._mdb["business"].execute(sql_u)
        except BaseException:
            logging.error("--------Error: %s" % traceback.format_exc())
            success = False
        return success, company_uid

    def queryCompanyCounts(self, filter_arg):
        """
        查询商户列表 数量
        :param filter_args: {
            "query": 模糊查询,
            "page": 页码,
            "per_page": 每页条数
            "status": active: 正常，closed: 封停, warning: 账户异常
        }
        :return:
        """
        page_info = {}
        filter_args = deepcopy(filter_arg)
        page = filter_args.pop("page", 0)
        per_page = filter_args.pop("per_page", 1)

        where_list = []
        query_str = filter_args.pop("query", None)
        status = filter_args.pop("status", None)

        for cl_key, value in filter_args.items():
            if value is not None:
                where_list.append((cl_key, value, "=", "and"))
        if query_str:
            sub_filter = [
                ("company_name", query_str, "like", "or"),
                ("phone", query_str, "like", "or"),
                ("email", query_str, "like", "or"),
                ("contacts_people", query_str, "like", "")
            ]
            where_list.append(("query_str", sub_filter, "sub", "and"))

        if status not in [None, ""]:
            where_list.append(("status", COMPANY_STATUS_DIC.get(status, 1), "=", ""))
        else:
            where_list.append(("status", "-3", "!=", ""))
        condition = {
            "where": where_list,
        }

        count_sql = self._sql._select("beacon_company", ["uuid) AS counts"], **condition)
        count_info = self._mdb["business"].fetchone(count_sql)
        total = count_info["counts"]
        if total:
            page_info = {
                "total": total,
                "total_page": int(total / per_page) + 1 if total % per_page else int(total / per_page)
            }
        return page_info

    def queryCompany(self, filter_arg, keyList=None, order_by=None):
        """
        查询商户列表
        :param filter_args: {
            "query": 模糊查询,
            "page": 页码,
            "per_page": 每页条数
            "uuid": 公司id,
            "company_uid_list": 商户id列表
            "status": active: 正常，closed: 封停, warning: 账户异常
            "createtime": 创建时间
        }
        :return:
        """
        if not keyList:
            keyList = ["uuid", "company_name", "phone", "contacts_people", "email", "status", "address"]
        filter_args = deepcopy(filter_arg)
        page = filter_args.pop("page", 0)
        per_page = filter_args.pop("per_page", 1)
        where_list = []
        query_str = filter_args.pop("query", None)
        status = filter_args.pop("status", None)
        company_uid_list = filter_args.pop("company_uid_list", None)
        for cl_key, value in filter_args.items():
            if value is not None:
                where_list.append((cl_key, value, "=", "and"))
        if query_str:
            sub_filter = [
                ("company_name", query_str, "like", "or"),
                ("phone", query_str, "like", "or"),
                ("email", query_str, "like", "or"),
                ("contacts_people", query_str, "like", "")
            ]
            where_list.append(("query_str", sub_filter, "sub", "and"))

        if company_uid_list:
            if len(company_uid_list) > 1:
                where_list.append(("uuid", tuple(company_uid_list), "in", "and"))
            else:
                where_list.append(("uuid", company_uid_list[0], "=", "and"))

        if status not in [None, ""]:
            where_list.append(("status", COMPANY_STATUS_DIC.get(status, 1), "=", ""))

        if not order_by:
            order_by = [("createtime", "DESC")]
        condition = {
            "where": where_list,
            "order": order_by
        }
        if page:
            limit_start = (page - 1) * per_page
            condition["limit"] = (limit_start, per_page)
        query_sql = self._sql._select("beacon_company", keyList, **condition)
        company_info = self._mdb["business"].fetchmany(query_sql)

        return company_info

    # ------------------------------- tools ------------------------------

    def checkCompanyName(self, company_name, query_list=None):
        """
        校验用户是否存在
        :param username:  "xxxxx"
        query_list: [ , , ]
        :return: user
        """
        if not query_list:
            query_list = ["company_name", "phone", "contacts_people", "status", "confirm_status"]
        condition = {
            "where": [("company_name", company_name, "=", "")],
            "limit": (0, 1)
        }
        u_sql = self._sql._select("beacon_company", query_list, **condition)
        company_inf = self._mdb["business"].fetchone(u_sql)
        return company_inf




class BaseModel(object):
    """
    基础操作模块 普通累通常继承此类，方便自动获取数据库、缓存、等操作对象
    主要应用于业务代码即时实例化对象的类上，让这些动态使用的类，继承此类
    """

    def __init__(self, handel_mod):
        """
        初始化 数据库、缓存、阿里短信发送等操作对象
        :param handel_mod: request handel (view层)对象
        """
        # self._mongo = handel_mod._mongo
        self._mdb = handel_mod._mdb
        self._rsdb = handel_mod._rsdb
        self._sql = handel_mod._sql
        # self._mq = handel_mod._mq

    def getMd5(self, data):
        """"""
        return getMd5(data)

    def any2str(self, data):
        return union2str(data)

    def json_encode_dump(self, data):
        return json_encode_dump(data)

    def trans_oss_file(self, items_info):
        """
        oss 文件获取访问地址
        :param items_info:
        :return:
        """
        for item in items_info:
            temp_upd = {}
            for i_key, i_value in item.items():
                if "oss_key" in i_key:
                    if i_value:
                        # 发现oss对象
                        temp_upd[i_key.replace("_oss_key", "")] = ossobj.sign_url(i_value)
                    else:
                        temp_upd[i_key.replace("_oss_key", "")] = ""
            item.update(temp_upd)
        return items_info


    async def fetch_rpc(self, req, language=""):
        """
        fetch url
        with json decode
        :param req: HTTPRequest object
        :param language: local-language
        :return: result
        """

        response = await fetch_rpc(req, language)
        return response

    def buildingRequest(self, url, method="GET", headers={}, req_body={}, acc_rpc_time_out=10, validate_cert=False):
        """
        :param url: url address
        :param method: GET/POST/..
        :param headers: { "KEY": VALUE}
        :param req_body: {"key1": value1, "keys": value2}
        :param acc_rpc_time_out: default 10 sec
        :param validate_cert: need cert check
        :return: req object
        """
        return buildingRequest(url, method=method, headers=headers,
                               req_body=req_body,
                               acc_rpc_time_out=acc_rpc_time_out,
                               validate_cert=validate_cert)

    def make_rpc_signature(self, params):
        """
        获取 rpc 调用 签名
        :param params:
        :return:
        """
        return make_rpc_sign(params)


