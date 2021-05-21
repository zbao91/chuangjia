# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   files
    Description:
    Author:      bzq
    Date:        2021/04/22
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

from utils.httpmixin import HTTPContent
from apps.handler import BaseHandler, UserBaseHandler
from config.config import SECRETE_KEY
from core.cache import *
from pdf2docx import Converter


class CreateCategory(UserBaseHandler):
    """
    创建文件夹分类
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
        category_name = self._xss(self.get_argument("category_name", ""))
        if not category_name:
            result["code"] = 0
            result["msg"] = "请输入分类名称"
            self.write(result)
            self.finish()
            return
        # 获取该人员的数据
        sql = " select count(1) as counter  from file_categories " \
              " where name = '%s' and status = 1 "%(category_name)
        data = self._mdb.get(sql).get("counter", 0)
        if data:
            result["code"] = 0
            result["msg"] = "该文件分类已存在"
            self.write(result)
            self.finish()
            return

        sql = " select max(sort_order) as sort_order from file_categories" \
              " where status = 1 "
        data = self._mdb.get(sql)
        sort_order = data.get("sort_order", 0) + 1 if data.get("sort_order", 0) else 1
        insert_dict = {
            "name": category_name,
            "sort_order": sort_order
        }
        sql = self._sql._insert("file_categories", insert_dict)
        self._mwdb.execute(sql)
        self.write(result)
        self.finish()
        return

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
        category_id = self._xss(self.get_argument("category_id", ""))
        if not folder_name or not category_id:
            result["code"] = 0
            result["msg"] = "请输入文件夹名称并选择分类"
            self.write(result)
            self.finish()
            return
        # 获取该人员的数据
        sql = " select count(1) as counter  from file_folders a join file_category_folder_rel b on a.id = b.folder_id " \
              " where a.name = '%s' and b.category_id = '%s' and a.status = 1 and b.status = 1 "%(folder_name, category_id)
        data = self._mdb.get(sql).get("counter", 0)
        if data:
            result["code"] = 0
            result["msg"] = "该分类下，该文件夹已存在，请重新输入文件夹名称"
            self.write(result)
            self.finish()
            return

        sql = " select max(sort_order) as sort_order from file_category_folder_rel" \
              " where category_id = '%s' and status = 1 " % (category_id)
        data = self._mdb.get(sql)
        sort_order = data.get("sort_order", 0) + 1 if data.get("sort_order", 0) else 1
        insert_dict = {
            "name": folder_name,
        }
        sql = self._sql._insert("file_folders", insert_dict)
        folder_id = self._mdb.execute(sql)
        insert_dict = {
            "folder_id": folder_id,
            "category_id": category_id,
            "sort_order": sort_order,

        }
        sql = self._sql._insert("file_category_folder_rel", insert_dict)
        self._mdb.execute(sql)
        cwd = os.getcwd()
        # folder_path = os.path.join(cwd, "files", folder_name)
        # os.mkdir(folder_path)
        self.write(result)
        self.finish()
        return

class CategoryList(UserBaseHandler):
    """
        分类列表
    """
    login = False
    def get(self):

        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        sql = " select id as category_id, name as category_name from file_categories " \
              " where status = 1 order by sort_order asc "
        result = self._mdb.query(sql)
        response["data"] = result
        self.write(response)
        self.finish()
        return

class CategorFolderList(UserBaseHandler):
    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        sql = " select a.name as folder_name, b.sort_order, c.name as category_name, a.id as folder_id, c.id as category_id " \
              " from file_folders a join file_category_folder_rel b on a.id = b.folder_id " \
              " join file_categories c on c.id = b.category_id " \
              " where a.status = 1 and b.status = 1 and c.status = 1  " \
              " order by b.sort_order asc, c.sort_order asc "
        result = self._mdb.query(sql)
        folder_list = []
        index_dict = {}
        index = 0
        for i in result:
            folder_name = i.get("folder_name")
            category_name = i.get("category_name")
            category_id = i.get("category_id")
            sort_order = i.get("sort_order")
            folder_id = i.get("folder_id")
            folder_dict = {
                            "folder_name": folder_name,
                            "folder_id": folder_id,
                            "sort_order": sort_order
                            }
            if not category_name in index_dict:
                index_dict[category_name] = index
                tmp_dict = {
                    "category_name": category_name,
                    "category_id": category_id,
                    "category_index": index,
                    "data": [folder_dict]
                }
                folder_list.append(tmp_dict)
                index += 1
            else:
                folder_list[index_dict.get(category_name)]["data"].append(folder_dict)
        response["data"] = folder_list
        self.write(response)
        self.finish()
        return

class UpdateCategoryAndFolder(UserBaseHandler):
    def post(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        deleted_category = self._xss(self.get_argument("deleted_categories", ""))
        delete_folders = self._xss(self.get_argument("delete_folders", ""))
        folder_category = self._xss(self.get_argument("folder_categories", ""))


        deleted_categorys = deleted_category.split(",")
        delete_folders = delete_folders.split(",")
        folder_categorys = folder_category.split("|")

        # 先删除category
        for category_id in deleted_categorys:
            condition = {
                "where": [("id", category_id, "=", "and"), ("status", '1', "=", "")],
            }
            update_dict = {
                "status": -1,
                "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
            }
            sql = self._sql._update("file_categories", update_dict, **condition)
            self._mwdb.execute(sql)

            condition = {
                "where": [("category_id", category_id, "=", "and"), ("status", '1', "=", "")],
            }
            update_dict = {
                "status": -1,
                "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
            }
            sql = self._sql._update("file_category_folder_rel", update_dict, **condition)
            self._mwdb.execute(sql)

        # 在删除folders和对应的文件
        for folder_id in delete_folders:
            condition = {
                "where": [("id", folder_id, "=", "and"), ("status", '1', "=", "")],
            }
            update_dict = {
                "status": -1,
                "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
            }
            sql = self._sql._update("file_folders", update_dict, **condition)
            self._mwdb.execute(sql)

            condition = {
                "where": [("id", folder_id, "=", "and"), ("status", '1', "=", "")],
            }
            update_dict = {
                "status": -1,
                "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
            }
            sql = self._sql._update("file_files", update_dict, **condition)
            self._mwdb.execute(sql)

            condition = {
                "where": [("folder_id", folder_id, "=", "and"), ("status", '1', "=", "")],
            }
            update_dict = {
                "status": -1,
                "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
            }
            sql = self._sql._update("file_category_folder_rel", update_dict, **condition)
            self._mwdb.execute(sql)

        # 然后更新数据
        for folder_category_info in folder_categorys:
            if not folder_category_info:
                continue
            category_id, folder_ids_str = folder_category_info.split("_")
            folder_ids_list = folder_ids_str.split(",")
            for index, folder_id in enumerate(folder_ids_list):
                condition = {
                    "where": [("folder_id", folder_id, "=", "and"), ("status", '1', "=", "")],
                }
                update_dict = {
                    "category_id": category_id,
                    "sort_order": index,
                    "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
                }
                sql = self._sql._update("file_category_folder_rel", update_dict, **condition)
                self._mwdb.execute(sql)

        self.write(response)
        self.finish()
        return

class ReSortFolder(UserBaseHandler):

    def post(self):
        result = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        new_order_str = self._xss(self.get_argument("new_order", ""))
        new_order = new_order_str.split("|")
        for i in new_order:
            folder_id, sort_order  = i.split("_")
            condition = {
                "where": [("folder_id", folder_id, "=", "and"), ("status", '1', "=", "")],
            }
            update_dict = {
                "sort_order": sort_order,
                "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
            }
            sql = self._sql._update("file_category_folder_rel", update_dict, **condition)
            self._mwdb.execute(sql)
        self.write(result)
        self.finish()
        return

class UploadFiles(UserBaseHandler):

    def post(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        type = self._xss(self.get_argument("type", ""))
        file_name = self._xss(self.get_argument("file_name", ""))
        file_body = self.request.files['file'][0]
        if not file_name:
            response["code"] = 0
            response["msg"] = "上传失败"
            self.write(response)
            self.finish()
            return
        file_type = file_name.split(".")[-1]
        if file_type == "doc":
            file_name = file_name.replace("doc", "docx")

        uid = uuid.uuid4()
        new_file_name = str(uid).replace("-", "") + "_" + file_name
        # 保存文件
        cwd = os.getcwd()
        if type:
            dir_path = os.path.join(cwd, "files", type)
            file_path = os.path.join(cwd, "files", type, new_file_name)
        else:
            dir_path = os.path.join(cwd, "files", type)
            file_path = os.path.join(cwd, "files", new_file_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        output_file = open(file_path , 'wb')
        output_file.write(file_body.body)

        # 格式转化
        if file_type == 'pdf':
            word_file_path = file_path.replace('pdf', "docx")
            cv = Converter(file_path)
            cv.convert(word_file_path, start=0, end=None)
            cv.close()


        # 保存数据
        insert_dict = {
            "file_name": file_name,
            "uid": str(uid).replace("-", ""),
            "type": type,
            "path": file_path,
            "create_time": datetime.datetime.today(),
        }
        sql = self._sql._insert("files_upload_history", insert_dict)
        self._mwdb.execute(sql)
        response["data"] = {
            "file_path": file_path,
            "uid": str(uid).replace("-", ""),
            "file_name": file_name
        }
        self.write(response)
        self.finish()
        return

class UploadFilesOLD(UserBaseHandler):

    def post(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        folder_id = self._xss(self.get_argument("folder_id", ""))
        file_name = self._xss(self.get_argument("file_name", ""))
        file_path = self._xss(self.get_argument("file_path", ""))
        file_uid = self._xss(self.get_argument("file_uid", ""))
        sql = " select name from file_folders where id = '%s' "%folder_id
        result = self._mdb.get(sql)
        if not result:
            response["code"] = 0
            response["msg"] = "数据获取失败"
            self.write(response)
            self.finish()
            return
        # 保存文件
        # 保存数据
        insert_dict = {
            "folder_id": folder_id,
            "file_path": file_path,
            "file_uid": file_uid,
            "name": file_name,
            "create_time": datetime.datetime.today(),
        }
        sql = self._sql._insert("file_files", insert_dict)
        self._mwdb.execute(sql)
        self.write(response)
        self.finish()
        return

class FilesList(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }
        folder_id = self._xss(self.get_argument("folder_id", ""))
        keyword = self._xss(self.get_argument("keyword", ""))
        sort_column = self._xss(self.get_argument("sort_field", "create_time")) if self._xss(self.get_argument("sort_field", "create_time")) else "create_time"
        sort_order = self._xss(self.get_argument("sort_order", "desc"))
        if sort_order.startswith("asc"):
            sort_order = "asc"
        else:
            sort_order = "desc"
        page = self._xss(self.get_argument("page_number", "1"))
        start, end = self.pagination(page)
        condition = {
            "where": [("folder_id", folder_id, "=", "and"), ("status", '1', "=", "")],
            "limit": [start, end],
            "order": " %s %s "%(sort_column, sort_order)
        }
        keyList = [" `name` as `file_name` ", "id as file_id", "folder_id", "create_time", "file_path"]
        if keyword:
            condition["where"].insert(0, ("name", "%%{}%%".format(keyword), "==", "and"))
        sql = self._sql._select("file_files", keyList, **condition)

        sql_str, sql_value = sql
        sql = (sql_str.replace("==", "like"), sql_value)
        result = self._mdb.query(sql)
        for i in result:
            file_dir = i["file_path"].replace(os.getcwd(), "").split("/")[2:] if i["file_path"] else ""
            i["file_path"] = "http://localhost:9023/download/" + "/".join(file_dir)
            i["file_type"] = i["file_path"].split(".")[-1] if "." in i["file_path"] else ""
            i["create_time"] = self.datetime_to_string(i["create_time"], "%Y-%m-%d %H:%M:%S")

        condition = {
            "where": [("folder_id", folder_id, "=", "and"), ("status", '1', "=", "")],
        }
        if keyword:
            condition["where"].insert(0, ("name", "%%{}%%".format(keyword), "==", "and"))
        keyList = [" count(1) as counter"]
        sql = self._sql._select("file_files", keyList, **condition)
        sql_str, sql_value = sql
        sql = (sql_str.replace("==", "like"), sql_value)
        length = self._mdb.get(sql).get("counter")
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
        print(file_id)
        if not file_id:
            response["code"] = 0
            response["msg"] = "文件不存在"
            self.write(response)
            self.finish()
            return
        condition = {
            "where": [("id", file_id, "=", "and"), ("status", '1', "=", "")],
        }
        update_dict = {
            "status": -1,
            "modify_time": self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        }
        sql = self._sql._update("file_files", update_dict, **condition)



        self._mwdb.execute(sql)
        self.write(response)
        self.finish()
        return

class DownloadFile(UserBaseHandler):
    def get(self):
        file_name = '/files/创建文件夹/WX20210326-112820@2x.png'
        buf_size = 4096
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename=' + file_name)
        print(file_name)
        with open(file_name, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()
        return