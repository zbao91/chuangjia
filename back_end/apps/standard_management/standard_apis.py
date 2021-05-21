# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   files
    Description:
    Author:      bzq
    Date:        2021/04/25
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
import json
import requests
import copy

from utils.httpmixin import HTTPContent
from apps.handler import BaseHandler, UserBaseHandler
from config.config import SECRETE_KEY
from core.cache import *

class CreateFolder(UserBaseHandler):
    """
    创建文件夹分类
    """
    login = True
    def post(self):
        result = {
            "code": 1,
            "msg":"成功",
            "time": int(time.time()),
            "data": None,
        }
        # 获取参数
        folder_name = self._xss(self.get_argument("folder_name", ""))
        parent_folder_id = self._xss(self.get_argument("parent_folder_id", ""))
        if not folder_name:
            result["code"] = 0
            result["msg"] = "输入目录名称"
            self.write(result)
            self.finish()
            return
        # 获取该人员的数据
        sql_condition = " from standard_folders where name = '%s' and status = 1 "%(folder_name)
        if parent_folder_id:
            sql_condition += " and parent_folder_id = '%s' "%parent_folder_id
        counter_sql = " select count(1) as counter " + sql_condition
        print(counter_sql)
        data = self._mdb.get(counter_sql).get("counter", 0)
        if data:
            result["code"] = 0
            result["msg"] = "该目录已存在，请重新确认后重新添加"
            self.write(result)
            self.finish()
            return

        sort_order_sql = " select max(sort_order) as sort_order  " + sql_condition
        print(sort_order_sql)
        sort_res = self._mdb.get(sort_order_sql)
        sort_order = sort_res.get("sort_order", 0) + 1 if sort_res.get("sort_order") else 1
        print(sort_order)
        insert_dict = {
            "name": folder_name,
            "parent_folder_id": parent_folder_id if parent_folder_id else -1,
            "sort_order": sort_order,
            "create_time": datetime.datetime.today(),
        }
        sql = self._sql._insert("standard_folders", insert_dict)
        folder_id = self._mdb.execute(sql)
        # 创建文件夹
        cwd = os.getcwd()
        if parent_folder_id:
            sql = " select name from standard_folders where id = '%s' "%parent_folder_id
            parent_category_name = self._mdb.get(sql).get("name")
            folder_path = os.path.join(cwd, "files", "standard", parent_category_name, folder_name)
        else:
            folder_path = os.path.join(cwd, "files", "standard", folder_name)
        os.makedirs(folder_path)
        self.write(result)
        self.finish()
        return


class EditFolder(UserBaseHandler):
    """
    创建文件夹分类
    """
    login = True
    def post(self):
        result = {
            "code": 1,
            "msg":"成功",
            "time": int(time.time()),
            "data": None,
        }
        # 获取参数
        folder_name = self._xss(self.get_argument("folder_name", ""))
        folder_id = self._xss(self.get_argument("folder_id", ""))
        if not folder_name or not folder_id:
            result["code"] = 0
            result["msg"] = "输入目录名称"
            self.write(result)
            self.finish()
            return
        current_time = self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sql = " update standard_folders set name = '%s', modify_time = '%s' where id = '%s'  "%(folder_name, current_time, folder_id)
        self._mwdb.execute(sql)
        self.write(result)
        self.finish()
        return

class DeleteFolder(UserBaseHandler):
    """
    创建文件夹分类
    """
    login = True
    def post(self):
        result = {
            "code": 1,
            "msg":"成功",
            "time": int(time.time()),
            "data": None,
        }
        # 获取参数
        folder_id = self._xss(self.get_argument("folder_id", ""))
        if not folder_id:
            result["code"] = 0
            result["msg"] = "请选择目录目录"
            self.write(result)
            self.finish()
            return
        current_time = self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sql = " update standard_folders set status = '-1', modify_time = '%s' where id = '%s'  "%(current_time, folder_id)
        self._mwdb.execute(sql)
        self.write(result)
        self.finish()
        return


class FolderList(UserBaseHandler):
    """
        目录列表
    """
    login = False
    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        # 先获取母目录
        sql = " select id as folder_id, name as folder_name from standard_folders " \
              " where status = 1 and parent_folder_id = '-1' order by sort_order asc "
        parent_folders = self._mdb.query(sql)
        for i in parent_folders:
            parent_folder_id = i.get("folder_id")
            sql = " select id as folder_id, name as folder_name from standard_folders where status = 1 and parent_folder_id = '%s' order by sort_order asc "%parent_folder_id
            i["children"] = self._mdb.query(sql)
        response["data"] = parent_folders
        self.write(response)
        self.finish()
        return

class UploadStandardFile(UserBaseHandler):

    def post(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        # 获取参数
        standard_id = self._xss(self.get_argument("standard_id", ""))
        file_path = self._xss(self.get_argument("file_path", ""))
        file_uid = self._xss(self.get_argument("file_uid", ""))
        name = self._xss(self.get_argument("name", ""))
        folder_id = self._xss(self.get_argument("folder_id", ""))
        child_folder_id = self._xss(self.get_argument("child_folder_id", ""))
        version = self._xss(self.get_argument("version", ""))

        if child_folder_id:
            folder_id = child_folder_id

        # 保存数据
        insert_dict = {
            "folder_id": folder_id,
            "name": name,
            "version": version,
            "standard_id": standard_id,
            "file_path": file_path,
            "file_uid": file_uid,
            "create_time": datetime.datetime.today(),
        }
        sql = self._sql._insert("standard_files", insert_dict)
        self._mwdb.execute(sql)
        self.write(response)
        self.finish()
        return

class StandardFileList(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }
        folder_id = self._xss(self.get_argument("folder_id", ""))
        child_folder_id = self._xss(self.get_argument("child_folder_id", ""))
        search_keyword = self._xss(self.get_argument("search_keyword", ""))
        search_standard_id = self._xss(self.get_argument("search_standard_id", ""))
        sort_column = self._xss(self.get_argument("sort_field", "create_time")) if self._xss(
            self.get_argument("sort_field", "create_time")) else "create_time"
        sort_order = self._xss(self.get_argument("sort_order", "desc"))
        if sort_order.startswith("asc"):
            sort_order = "asc"
        else:
            sort_order = "desc"
        page = self._xss(self.get_argument("page_number", "1"))
        start, end = self.pagination(page)
        # 构建sql
        condition_sql = " from standard_files where status = 1 "
        if child_folder_id:
            condition_sql += " and folder_id = '%s' "%child_folder_id

        if not child_folder_id and folder_id:
            sql = " select id from standard_folders where parent_folder_id = '%s' "%folder_id
            folder_res = self._mdb.query(sql)
            folder_ids = [i.get("id") for i in folder_res]
            folder_ids.append(folder_id)
            folder_ids = [str(i) for i in folder_ids]
            condition_sql += " and folder_id in ('%s') " %("','".join(folder_ids))

        if search_keyword:
            condition_sql += " and name like '%%{}%%' ".format(search_keyword)

        if search_standard_id:
            condition_sql += " and standard_id like '%%{}%%' ".format(search_standard_id)

        condition_sql += " order by %s %s "%(sort_column, sort_order)
        condition_sql += " limit %s, %s " % (start, end)
        sql = " select standard_id, name as standard_name, file_path, version, create_time, id as file_id  " + condition_sql
        length_sql = "select count(1) as counter " + condition_sql
        result = self._mdb.query(sql)
        index = 1
        for i in result:
            i["index"] = index + start
            i["create_time"] = self.datetime_to_string(i["create_time"], "%Y-%m-%d %H:%M:%S") if i["create_time"] else i["create_time"]
            file_dir = i["file_path"].replace(os.getcwd(), "").split("/")[2:]
            i["file_path"] = "http://localhost:9023/download/" + "/".join(file_dir)
            index += 1
        length = self._mdb.get(length_sql).get("counter")
        response["data"]["content"] = result
        response["data"]["total_elements"] = length
        self.write(response)
        self.finish()
        return

class DeleteFile(UserBaseHandler):

    def post(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }
        file_id = self._xss(self.get_argument("file_id", ""))
        # 构建sql
        sql = " select *  from standard_files where id = '%s' "%file_id
        counter = self._mdb.get(sql)
        if not counter:
            response["code"] = 0
            response["msg"] = "该文件不存在"
            self.write(response)
            self.finish()
            return
        update_sql = " update standard_files set status = -1 where id = '%s' "%file_id
        self._mwdb.execute(update_sql)
        self.write(response)
        self.finish()
        return

class FileDetail(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }
        file_id = self._xss(self.get_argument("file_id", ""))
        # 构建sql
        sql = " select id as file_id, standard_id, name , version, folder_id, file_path from standard_files where id = '%s' "%file_id
        data = self._mdb.get(sql)
        if not data:
            response["code"] = 0
            response["msg"] = "该文件不存在"
            self.write(response)
            self.finish()
            return

        # 获取文件
        folder_id = data.get("folder_id")
        folder_sql = " select * from standard_folders where id = '%s' "%folder_id
        folder_info = self._mdb.get(folder_sql)
        if folder_info:
            parent_folder_id = folder_info.get("parent_folder_id")
            folder_name = folder_info.get("name")
            data["child_folder_id"] = None
            data["child_folder_name"] = None
            if int(parent_folder_id) != -1:
                data["folder_id"] = folder_id
                data["child_folder_id"] = folder_name
                data["child_folder_name"] = folder_id
                folder_sql = " select * from standard_folders where id = '%s' " % parent_folder_id
                folder_info = self._mdb.get(folder_sql)
                if folder_info:
                    data["folder_id"] = parent_folder_id
                    folder_name = folder_info.get("name")
                    data["folder_name"] = folder_name

        file_dir = data["file_path"].replace(os.getcwd(), "").split("/")[2:]
        data["file_path"] = "http://localhost:9023/download/" + "/".join(file_dir)

        response["data"] = data
        self.write(response)
        self.finish()
        return