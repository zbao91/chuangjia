# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   handler
    Description: 
    Author:      wzj
    Date:        2019/7/23
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import asyncio
import collections
import datetime
import logging
import time
import traceback
import ujson
import hashlib
import uuid
from copy import deepcopy, copy
from typing import Sequence
from typing import Union

from tornado.web import HTTPError
from tornado.web import RequestHandler
from dbdriver import sql_format, tdb

from config.config import DEBUG
from core.args import deauth
from core.errors import MissArgError, BadArgError, BaseError, UserRoleError, LoginTokenException, LoginNeedException, RolePermmisonExecption
from core.func import remove_html_br
from dbdriver import rdb

arg_name = {
    'pid': '零件号',
    'brandCode': '品牌',
    'brand': '品牌',
    'vin': '车架号'
}

app_args = ['JPushID','deviceid', 'time', 'device', 'appname', 'hash', 'hashid', 'version']

show_args = ['deviceid', 'version']


class BaseHandler(RequestHandler):
    """
    handler基类
    """
    login = False
    role = None
    operate = None
    lever = 'info'
    url_name = {}
    _a_args = {}

    def _xss(self, args):
        return args

    _sql = sql_format

    def get_int_argument(self, arguement_name, default=None, show_arguement_name=None)->int:
        argu = self.get_argument(arguement_name, None) or default
        if argu is None:
            raise MissArgError(show_arguement_name or arguement_name)
        else:
            try:
                arg = int(argu)
            except ValueError:
                if show_arguement_name:
                    msg = '请确认参数{arguement_name}为整数'.format(arguement_name=show_arguement_name)
                else:
                    msg = '请确认参数{arguement_name}为整数'.format(arguement_name=arguement_name)
                raise BadArgError(msg)
            else:
                return arg

    def get_str_argument(self, arguement_name, default=None, show_arguement_name=None)->str:
        argu = self.get_argument(arguement_name, None) or default
        if argu is None:
            raise MissArgError(show_arguement_name or arguement_name)
        return argu

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.result = {
            'code': 1,
            'msg': '成功',
            'time': int(time.time())
        }
        super(BaseHandler, self).__init__(application, request, **kwargs)
        if DEBUG:
            logging.error('--------输入参数---------')
            logging.error(self.request.arguments)
        self.parse_args()
        self.uid = self.get_argument('uid', '')
        self.yc_id = self.uid
        self._loged = False
        self._sql = sql_format
        self._mdb = tdb
        self._mwdb = tdb

    def prepare(self):
        # 用户已经登录，但登录是否有效还需check_login判断
        login = self.login
        role = self.role
        if login:
            username = self.request.headers.get("user")
            token = self.request.headers.get("token")
            if rdb.get("%s_token" % username) != token:
                raise LoginNeedException('请重新登录')
            return username

        if role:
            username = self.request.headers.get("user")
            user_role = rdb.get("%s_role" % username)
            if not user_role in role:
                raise RolePermmisonExecption('该账号无次权限')
            return username




    def _get_all_args(self):
        if self._a_args:
            return self._a_args
        else:
            args = {}
            query = deepcopy(self.request.arguments)
            for arg_name in query.keys():
                arg_value = self.get_argument(arg_name)
                args[arg_name] = arg_value
            self._a_args = args
            return args

    def check_args(self):
        pass

    def parse_args(self):
        self.check_args()
        args = self._get_all_args()
        if 'auth' in args:
            try:
                auth = deauth(args.pop('auth'))
                args.update(auth)
            except Exception:
                logging.error(traceback.format_exc() + '\n' + str(self.request.arguments))
        app_arg_map, rpc_arg_map = {}, {}
        log_data = []
        for key, value in args.items():
            if key in app_args:
                app_arg_map[key] = value
            else:
                if key == 'uid':
                    rpc_arg_map['yc_id'] = value
                    app_arg_map['yc_id'] = value
                    app_arg_map['uid'] = value
                elif key == 'brand':
                    rpc_arg_map['brandCode'] = value
                    app_arg_map['brandCode'] = value
                elif key == 'code':
                    rpc_arg_map['brandCode'] = value
                    app_arg_map['brandCode'] = value
                else:
                    rpc_arg_map[key] = value
            if key in show_args or key not in app_args:
                log_data.append(arg_name.get(key, key) + ':[' + str(value) + ']')
        self.qdict = rpc_arg_map
        self.adict = app_arg_map
        self.log_data = '-'.join(log_data) # 运营看
        temp = rpc_arg_map.copy()
        temp.update(self.adict)
        temp.pop('yc_id', '')
        temp.pop('uid', '')
        self.log_args = ujson.dumps(temp)  # 后端看

    def clear_write(self):
        self._write_buffer = []

    def write(self, chunk):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
        self.set_header("Access-Control-Allow-Headers", "token, content-type, user-token, username, role, "
                                                        "authorization, Authorization, Content-Type, Access-Control-Allow-Origin, "
                                                        "Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods,  x-requested-with ")
        self.set_header("X-Requested-With", "XMLHttpRequest")
        self.clear_write()
        if isinstance(chunk, dict):
            self.return_msg = chunk.get('msg', '无提示')
            self.return_code = chunk.get('code', -100)
        if self.get_status() == 200:
            super().write(self.formate_datatime(chunk))
        else:
            super().write(chunk)
        if DEBUG:
            logging.error(chunk)

    def simplewrite(self, code=1, msg='成功', data=None, **kwargs):
        res = {
            'code': code,
            'msg': msg,
            'time': int(time.time()),
            'data': data
        }
        # res['data'] = {} if data is None else data
        res.update(kwargs)
        self.write(res)

    def datetime_to_string(self,dt, formate="%m-%d %H:%M"):
        c_time = dt.strftime(formate)
        return c_time

    def get_today_str(self):
        return  self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")


    def formate_datatime(self, rd, formate="%m-%d %H:%M"):
        # 顺便处理auth
        data = copy(rd)
        if isinstance(rd, dict):
            for key, value in rd.copy().items():
                if isinstance(value, str):
                    if key == 'mcid':
                        data['auth'] = rd.get('mcid')
                    else:
                        data[key] = remove_html_br(value)
                if isinstance(value, collections.Mapping):
                    data[key] = self.formate_datatime(value, formate)
                if isinstance(value, datetime.datetime):
                    data[key] = self.datetime_to_string(value, formate)
                if isinstance(value, list):
                    data[key] = [self.formate_datatime(item) for item in value]
        if isinstance(rd, list):
            data = [self.formate_datatime(item) for item in rd]
        return data


    def write_error(self, status_code, **kwargs):
        self.set_header('Content-Type', 'application/json')

        # serve_traceback的值依赖于debug模式
        if "exc_info" in kwargs:
            _, e, tb = kwargs['exc_info']
            self.set_status(200)
            self.simplewrite(code=getattr(e, 'code', 0), msg=getattr(e, 'msg', '服务异常'))
        else:
            self.finish(ujson.dumps({'msg':self._reason, 'code': status_code}))

    def finish(self, chunk: Union[str, bytes, dict] = None):
        if not self._write_buffer:
            self.simplewrite()
        if not self._loged:
            self.setUserRecords()
        super().finish(chunk)

    def setUserRecords(self):
        """
            * 表示新增 或有变化的字段
            yc_id:           cats--user--uid 用户唯一标识                                         非空              ""
           * yc_status:      用户当前帐号状态，如： 账户有效期等 在当前业务对结果输出有影响的信息          选填              "{}"
            operate:         相关业务／接口 操作方式 (需保证运营人员明显看懂)                          非空              ""
           * operate_key:    当前调用接口 如 user/info                                            不用传               ""
           * args:           当前接口的所有参数，100% 全记录，目的: 可直接模拟请求                     不用传             "{}"
           * version:        应用版本号                                                          不用传              “”
            data:            相关参数中文说明信息 (需保证运营人员可看懂)                              选填               ""
           * lever:          日志等级: info/error/warning/idiot/danger: 正常调用/发生异常/警告/参数错误/危险情况      选填              ""
            ways:            请求来源设备 web/ios/android/h5                                     web端使用"web", app端 使用接口中的device字段: ios/android/..
           * errorlog:       程序抛出异常(或程序中间关键参数的值)                                            无异常不记录       “” 或 "{}"
           * table:          将要存储的日志表，为适应后期不同业务日志分表，设置此字段                    默认 user_log
           * app:            来源应用 007/qixiu/qipei
        """

        """
            数据格式说明
            operate：  主分支名称 - 相关数据 - 动作， 例： 零件号查询-零件替换件-查询
            data:      参数名1[参数值1], 参数名2[参数值2], 参数名3[参数值3]=执行结果／提示  例: 零件号[000043153208UT],品牌[porsche]=没有这个零件号信息
        """
        if not self.yc_id:
            # 如果yc_id 为空值, 不记录相关记录
            return
        try:
            # data中 ，所有value都必须为 String 类型
            real_ip = self.get_client_ip()
            data = {
                "yc_id": self.yc_id,
                "operate": self.find_url_name(),
                "operate_key": self.request.path,
                "lever": self.lever,
                "data": self.log_data,
                "yc_status": '',
                "ways": self.adict.get('device', 'unknow'),
                "table": 'user_log',
                "args": self.log_args,
                "app": 'qipei',
                "create_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),      # 发生时间
                "sip": real_ip,
                "errorlog": '',
            }
            # 就目前使用的redis中间件，存储字典类型会自动转换成字符串
            key = "user_records_app"
            rdb.lpush(key, ujson.dumps(data))
            self._loged = True
        except:
            logging.error(traceback.format_exc())

    def find_url_name(self):
        # for rule in self.application.default_router.rules:
        #     target_params = rule.matcher.match(self.request)
            # if target_params is not None:
            # logging.error(dir(self.application.find_handler(self.request)))
        return ''

    def get_client_ip(self):
        ip = self.request.headers.get("X-Forwarded-For",None)
        if ip is None or ip=='':
            ip = self.request.headers.get("X-Real-IP",'')
        if ip is None or ip=='':
            ip = self.request.headers.get("X-Client-Ip",'')
        if not ip:
            ip = self.request.remote_ip
        return ip.split(',')[0]

    def pagination(self, page_num, page_size=10):
        page_num = int(page_num)
        return (page_num - 1) * page_size, page_num * page_size






class UserBaseHandler(BaseHandler):
    """
    handler基类
    """
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def check_password(self, username, password):
        keyList = ["*"]
        condition = {
            "where": [("username", username, "=", "and"), ("status", '1', "=", "")],
        }
        sql = self._sql._select("user", keyList, **condition)
        data = self._mdb.get(sql)
        if not data: return False, "账号不存在"
        check_password = data.get("password")
        salt = data.get("salt")
        password += salt
        # 进行密码校验
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        if (check_password != hashed_password): return False, "密码错误，请确认后重新输入"
        return True, ""


    def create_password(self, password):
        salt = uuid.uuid4().hex
        password += salt
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        return hashed_password, salt

    def get_uid_by_username(self, username):
        uid = None
        # 获取申请id
        sql = " select id from user where username = '%s' and status = 1 " % (username)
        sql_res = self._mdb.get(sql)
        if sql_res:
            uid = sql_res.get("id")
        return uid