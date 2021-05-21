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

class ApplyImage(UserBaseHandler):

    def post(self):
        result = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }

        customer_name = self._xss(self.get_argument("customer_name", "")) # 客户名称
        id = self._xss(self.get_argument("id", ""))  # 图号id
        vehicle_model = self._xss(self.get_argument("vehicle_model", "")) # 车型号
        product_name = self._xss(self.get_argument("product_name", "")) # 产品名称
        product_cid = self._xss(self.get_argument("product_cid", "")) # 客户品号
        product_rule_id = self._xss(self.get_argument("product_rule_id", ""))  # 规则id
        product_description = self._xss(self.get_argument("product_description", ""))  # 配套描述
        applicant_username = self._xss(self.get_argument("applicant_username", ""))  # 客户名称
        product_diameter = self._xss(self.get_argument("product_diameter", ""))  # 尺寸信息
        product_length = self._xss(self.get_argument("product_length", ""))  # 尺寸信息

        # 获取申请id
        sql = " select id from user where username = '%s' and status = 1 "%(applicant_username)
        sql_res = self._mdb.get(sql)
        if sql_res:
            uid = sql_res.get("id")
        else:
            result["code"] = 0
            result["msg"] = "人员错误"
            self.write(result)
            self.finish()
            return

        if not customer_name or not vehicle_model or not product_name or not product_rule_id:
            result["code"] = 0
            result["msg"] = "请输入必填项"
            self.write(result)
            self.finish()
            return

        if id:
            # 图号已经存在
            sql = " update images set customer_name = '%s', product_cid = '%s', product_description = '%s', " \
                  " modify_time = '%s', editor_id = '%s' where id = '%s' "%(customer_name, product_cid, product_description,
                                                                            datetime.datetime.today(), uid, id)
            self._mwdb.execute(sql)
        else:
            # 图号不存在
            # 获取规则
            sql = " select * from images_rules where id = '%s' and status = 1 " % product_rule_id
            rule_res = self._mdb.get(sql)
            if not sql_res:
                result["code"] = 0
                result["msg"] = "请选择正确产品"
                self.write(result)
                self.finish()
                return
            product_rule_id = rule_res.get("id")
            product_rule_cid = rule_res.get("product_cid")
            # 获取index
            sql = " select product_rule_index as distincter from images where vehicle_model = '%s' and product_rule_id = '%s' " % (
            vehicle_model.strip(), product_rule_id)
            vehicle_index_res = self._mdb.query(sql)
            if vehicle_index_res:
                product_rule_index = vehicle_index_res[0].get("distincter")
            else:
                sql = " select count(distinct(vehicle_model)) as counter from images where product_rule_id = '%s' " % (
                    product_rule_id)
                vehicle_index_res = self._mdb.get(sql)
                product_rule_index = "%03d" % (int(vehicle_index_res.get("counter")))

            if product_length:
                product_rule_spec = "%02d" % int(product_diameter) + "%02d" % int(product_length)

            elif str(rule_res.get("has_auto_increase")) == "1":
                sql = " select count(1) as counter from images where vehicle_model = '%s' and status = 1 " % vehicle_model.strip()
                tmp_counter = int(self._mdb.get(sql).get("counter")) + 1
                product_rule_spec = '10%02d' % tmp_counter
            else:
                product_rule_spec = "1000"
            product_oid = "C" + product_rule_cid + product_rule_index + "-" + product_rule_spec

            insert_dict = {
                "customer_name": customer_name,
                "vehicle_model": vehicle_model,
                "product_name": product_name,
                "product_cid": product_cid,
                "product_oid": product_oid,
                "product_rule_id": product_rule_id,
                "product_rule_cid": product_rule_cid,
                "product_rule_index": product_rule_index,
                "product_rule_spec": product_rule_spec,
                "product_description": product_description,
                "application_status": 0,  # 审核通过：1； 未审核通过：0
                "applicant_id": uid,
                "create_time": datetime.datetime.today(),
            }

            sql = self._sql._insert("images", insert_dict)
            self._mdb.execute(sql)
        self.write(result)
        self.finish()
        return

class ImageApplicationList(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }

        customer_name = self._xss(self.get_argument("customer_name", "")) # 客户名称
        vehicle_model = self._xss(self.get_argument("vehicle_model", "")) # 车型号
        product_name = self._xss(self.get_argument("product_name", "")) # 产品名称
        applicant_name = self._xss(self.get_argument("applicant_name", ""))  # 申请人
        page = self._xss(self.get_argument("page", "1"))  # 产品名称

        start, end = self.pagination(page)
        condition_sql = " where application_status = '0' and status = '1' "


        # 获取申请id
        if applicant_name:
            sql = " select id from user where name like '%%%s%%' and status = 1 " % (applicant_name)
            sql_res = self._mdb.query(sql)
            if sql_res:
                uids = [str(i.get("id")) for i in sql_res]
                uids_str = "'" + "','".join(uids) + "'"
                condition_sql += " and applicant_id in (%s) "%uids_str
            else:
                condition_sql += " and applicant_id = -1 "

        # 客户名称
        if customer_name:
            condition_sql += " and customer_name like '%%%s%%' "%customer_name

        # 车型号
        if vehicle_model:
            condition_sql += " and vehicle_model like '%%%s%%' " % vehicle_model

        # 产品名称
        if product_name:
            condition_sql += " and product_name like '%%%s%%' " % product_name

        sql_count = " select count(1) as counter from images  " + condition_sql

        condition_sql += " order by create_time desc "
        condition_sql += " limit %s, %s "%(start, end)
        result_sql = " select * from images " + condition_sql
        sql_result = self._mdb.query(result_sql)
        sql_counter = self._mdb.get(sql_count).get("counter")



        for index, i in enumerate(sql_result):
            i["index"] = start + index + 1
            i["application_time"] = self.datetime_to_string(i["create_time"], "%Y-%m-%d")
            sql = " select name from user where id = '%s' and status = 1 " % (i["applicant_id"])
            sql_result_username = self._mdb.get(sql)
            if sql_result_username:
                i["applicant_name"] = sql_result_username.get("name")
            else:
                i["applicant_name"] = ""

        response["data"]["content"] = sql_result
        response["data"]["total_elements"] = sql_counter
        self.write(response)
        self.finish()
        return

class ImageApplicationPass(UserBaseHandler):

    def post(self):
        result = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }

        application_id = self._xss(self.get_argument("application_id", "")) # 申请号
        audit_username = self._xss(self.get_argument("audit_username", ""))  # 审核人用户名

        # 获取申请id
        sql = " select id from user where username = '%s' and status = 1 " % (audit_username)
        sql_res = self._mdb.get(sql)
        if sql_res:
            uid = sql_res.get("id")
        else:
            result["code"] = 0
            result["msg"] = "人员错误"
            self.write(result)
            self.finish()
            return

        current_time = self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sql = " update images set application_status = 1, modify_time = '%s', audit_id = '%s' where id = '%s' "%(current_time, uid, application_id)
        self._mwdb.execute(sql)
        self.write(result)
        self.finish()
        return

class ImageApplicationDeny(UserBaseHandler):

    def post(self):
        result = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }

        application_id = self._xss(self.get_argument("application_id", ""))  # 申请号
        audit_username = self._xss(self.get_argument("audit_username", ""))  # 审核人用户名

        # 获取申请id
        sql = " select id from user where username = '%s' and status = 1 " % (audit_username)
        sql_res = self._mdb.get(sql)
        if sql_res:
            uid = sql_res.get("id")
        else:
            result["code"] = 0
            result["msg"] = "人员错误"
            self.write(result)
            self.finish()
            return

        current_time = self.datetime_to_string(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sql = " update images set application_status = 2, modify_time = '%s', audit_id = '%s' where id = '%s' " % (
        current_time, uid, application_id)
        self._mwdb.execute(sql)
        self.write(result)
        self.finish()
        return

class ImageList(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }

        customer_name = self._xss(self.get_argument("customer_name", "")) # 客户名称
        vehicle_model = self._xss(self.get_argument("vehicle_model", "")) # 车型号
        product_name = self._xss(self.get_argument("product_name", "")) # 产品名称
        product_oid = self._xss(self.get_argument("product_oid", ""))  # 图号
        applicant_name = self._xss(self.get_argument("applicant_name", ""))  # 申请人姓名
        page = self._xss(self.get_argument("page", "1"))  # 产品名称

        start, end = self.pagination(page)
        condition_sql = " where application_status = '1' and status = '1' "

        # 客户名称
        if customer_name:
            condition_sql += " and customer_name like '%%%s%%' "%customer_name

        # 车型号
        if vehicle_model:
            condition_sql += " and vehicle_model like '%%%s%%' " % vehicle_model

        # 产品名称
        if product_name:
            condition_sql += " and product_name like '%%%s%%' " % product_name

        # 图号id
        if product_oid:
            condition_sql += " and product_oid like '%%%s%%' " % product_oid

        # 人员
        if applicant_name:
            sql = " select id from user where name like '%%%s%%' and status = 1 " % (applicant_name)
            sql_res = self._mdb.query(sql)
            if sql_res:
                uids = [str(i.get("id")) for i in sql_res]
                uids_str = "'" + "','".join(uids) + "'"
                condition_sql += " and applicant_id in (%s) " % uids_str
            else:
                condition_sql += " and applicant_id = -1 "


        sql_count = " select count(1) as counter from images  " + condition_sql

        condition_sql += " order by create_time desc "
        condition_sql += " limit %s, %s "%(start, end)
        result_sql = " select * from images " + condition_sql
        sql_result = self._mdb.query(result_sql)
        sql_counter = self._mdb.get(sql_count).get("counter")
        print(result_sql)

        for index, i in enumerate(sql_result):
            i["index"] = start + index + 1
            i["application_time"] = self.datetime_to_string(i["create_time"], "%Y-%m-%d")
            sql = " select name from user where id = '%s' and status = 1 " % (i["applicant_id"])
            sql_result_username = self._mdb.get(sql)
            if sql_result_username:
                i["applicant_name"] = sql_result_username.get("name")
            else:
                i["applicant_name"] = ""

        response["data"]["content"] = sql_result
        response["data"]["total_elements"] = sql_counter
        self.write(response)
        self.finish()
        return

class AddImageRule(UserBaseHandler):

    def post(self):
        result = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": None,
        }
        id = self._xss(self.get_argument("id", ""))  # 产品分类代号
        product_cid = self._xss(self.get_argument("product_cid", "")) # 产品分类代号
        product_name_chn = self._xss(self.get_argument("product_name_chn", "")) # 产品名（中文）
        product_name_en = self._xss(self.get_argument("product_name_en", ""))  # 产品名（英文）
        product_type = self._xss(self.get_argument("product_type", "")) # 产品类型
        product_remarks = self._xss(self.get_argument("product_remarks", ""))  # 产品备注
        has_dimension = self._xss(self.get_argument("has_dimension", "0"))  # 是否需要标注尺寸
        has_auto_increase = self._xss(self.get_argument("has_auto_increase", "0"))  # 是否需要四位顺延新增
        creator_username = self._xss(self.get_argument("creator_username", ""))  # 是否需要四位顺延新增

        # 获取申请id
        if not product_cid or not product_name_chn or not product_type:
            result["code"] = 0
            result["msg"] = "请输入必填项"
            self.write(result)
            self.finish()
            return

        product_cid = str(product_cid).upper()
        # 获取创建人信息
        uid = self.get_uid_by_username(creator_username)
        if not uid:
            result["code"] = 0
            result["msg"] = "人员信息错误"
            self.write(result)
            self.finish()
            return

        # product_cid不能重复
        if id:
            condition = {
                "where": [("id", id, "=", "and"), ("status", '1', "=", "")],
            }
            update_dict = {
                "product_cid": product_cid,
                "product_name_chn": product_name_chn,
                "product_name_en": product_name_en,
                "product_type": product_type,
                "product_remarks": product_remarks,
                "has_dimension": has_dimension,
                "has_auto_increase": has_auto_increase,
                "editor_id": uid,
                "modify_time": datetime.datetime.today(),
                "status": 1
            }
            sql = self._sql._update("images_rules", update_dict, **condition)
        else:
            sql = " select * from images_rules where product_cid = '%s' and status = 1 "%product_cid
            sql_result = self._mdb.get(sql)
            if sql_result:
                result["code"] = 0
                result["msg"] = "产品分类代号已存在"
                self.write(result)
                self.finish()
                return

            insert_dict = {
                "product_cid": product_cid,
                "product_name_chn": product_name_chn,
                "product_name_en": product_name_en,
                "product_type": product_type,
                "product_remarks": product_remarks,
                "has_dimension": has_dimension,
                "has_auto_increase": has_auto_increase,
                "creator_id": uid,
                "create_time": datetime.datetime.today(),
                "status": 1
            }

            sql = self._sql._insert("images_rules", insert_dict)
        self._mdb.execute(sql)
        self.write(result)
        self.finish()
        return

class ImageRuleList(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }

        product_name = self._xss(self.get_argument("product_name", "")) # 产品名称
        product_type = self._xss(self.get_argument("product_type", ""))  # 申请人
        page = self._xss(self.get_argument("page", "1"))  # 产品名称

        start, end = self.pagination(page)
        condition_sql = " where status = '1' "

        # 产品名称
        if product_name:
            condition_sql += " and ( product_name_chn like '%%%s%%' or product_name_en like '%%%s%%' ) " %(product_name, product_name)

        # 产品类型
        if product_type:
            condition_sql += " and product_type like '%%%s%%'  " % (product_type)

        sql_count = " select count(1) as counter from images_rules  " + condition_sql

        condition_sql += " order by create_time desc "
        condition_sql += " limit %s, %s "%(start, end)
        result_sql = " select * from images_rules " + condition_sql
        sql_result = self._mdb.query(result_sql)
        sql_counter = self._mdb.get(sql_count).get("counter")

        for index, i in enumerate(sql_result):
            i["index"] = start + index + 1

        response["data"]["content"] = sql_result
        response["data"]["total_elements"] = sql_counter
        self.write(response)
        self.finish()
        return

class DeleteImageRule(UserBaseHandler):

    def post(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }

        rule_id = self._xss(self.get_argument("rule_id", "")) # 产品名称
        editor_username = self._xss(self.get_argument("editor_username", ""))  # 申请人

        uid = self.get_uid_by_username(editor_username)
        if not uid:
            response["code"] = 0
            response["msg"] = "人员错误"
            self.write(response)
            self.finish()
            return

        sql = " update images_rules set status = -1, editor_id = '%s', modify_time = '%s' where id = '%s' "%(uid, self.get_today_str(), rule_id)
        self._mwdb.execute(sql)
        self.write(response)
        self.finish()
        return

class SearchRule(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": [],
        }

        keyword = self._xss(self.get_argument("keyword", "")) # 产品名称
        sql = " select id, product_name_chn, product_type, product_remarks, has_dimension, has_auto_increase from images_rules where status = 1 and product_name_chn = '%s'  "%keyword
        sql_result = self._mdb.get(sql)
        tmp_list = []
        if sql_result:
            tmp_dict = {
                "show_name": "%s （%s——%s）"%(sql_result.get("product_name_chn"), sql_result.get("product_type"), sql_result.get("product_remarks")),
                "name": sql_result.get("product_name_chn"),
                "id": sql_result.get("id"),
                "has_dimension": sql_result.get("has_dimension"),
                "has_auto_increase": sql_result.get("has_auto_increase"),
            }
            tmp_list.append(tmp_dict)
        else:
            sql = " select id, product_name_chn, product_type, product_remarks, has_dimension, has_auto_increase from images_rules where status = 1 and product_name_chn like '%%%s%%'  "%keyword
            sql_result = self._mdb.query(sql)
            for i in sql_result:
                id = i.get("id")
                name = "%s （%s——%s）"%(i.get("product_name_chn"), i.get("product_type"), i.get("product_remarks"))
                has_dimension = i.get("has_dimension")
                has_auto_increase = i.get("has_auto_increase")
                tmp_dict = {
                    "show_name": name,
                    "name": i.get("product_name_chn"),
                    "id": id,
                    "has_dimension": has_dimension,
                    "has_auto_increase": has_auto_increase,
                }
                tmp_list.append(tmp_dict)
        response["data"] = tmp_list
        self.write(response)
        self.finish()
        return

class ImageRuleDetails(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }

        rule_id = self._xss(self.get_argument("rule_id", "")) # 产品名称

        sql = " select product_cid, product_name_chn, product_name_en, product_type, product_remarks, has_dimension, has_auto_increase " \
              " from images_rules where id = '%s' and status = 1 "%rule_id
        sql_res = self._mdb.get(sql)


        response["data"] = sql_res
        self.write(response)
        self.finish()
        return


class DeleteImage(UserBaseHandler):

    def post(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }

        image_id = self._xss(self.get_argument("image_id", "")) # 产品名称
        editor_username = self._xss(self.get_argument("editor_username", ""))  # 申请人

        uid = self.get_uid_by_username(editor_username)
        if not uid:
            response["code"] = 0
            response["msg"] = "人员错误"
            self.write(response)
            self.finish()
            return

        sql = " update images set status = -1, editor_id = '%s', modify_time = '%s' where id = '%s' "%(uid, self.get_today_str(), image_id)
        self._mwdb.execute(sql)
        self.write(response)
        self.finish()
        return

class ImageDetail(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }

        image_id = self._xss(self.get_argument("image_id", "")) # 产品名称
        sql = " select * from images where id = '%s' "%image_id
        detail_info = self._mdb.get(sql)
        if not detail_info:
            response["code"] = 0
            response["msg"] = "图号不存在"
            self.write(response)
            self.finish()
            return

        product_rule_id = detail_info.get("product_rule_id")
        detail_info["product_rule_id"] = product_rule_id
        # 获取数据
        sql = " select id, product_name_chn, product_type, product_remarks, has_dimension, has_auto_increase from images_rules where status = 1 and id = '%s'  " % product_rule_id
        sql_result = self._mdb.get(sql)
        if sql_result:
            detail_info["show_name"] = "%s（%s——%s）" % (sql_result.get("product_name_chn"), sql_result.get("product_type"), sql_result.get("product_remarks"))
            detail_info["has_dimension"] = sql_result.get("has_dimension")
            if int(sql_result.get("has_dimension")) == 1:
                detail_info["product_diameter"] = detail_info["product_rule_spec"][:2]
                detail_info["product_length"] = detail_info["product_rule_spec"][2:]
        response["data"] = detail_info
        self.write(response)
        self.finish()
        return

class RuleDetail(UserBaseHandler):

    def get(self):
        response = {
            "code": 1,
            "msg": "成功",
            "time": int(time.time()),
            "data": {},
        }

        rule_id = self._xss(self.get_argument("rule_id", "")) # 产品名称
        sql = " select * from images_rules where id = '%s' "%rule_id
        print(sql)
        detail_info = self._mdb.get(sql)
        if not detail_info:
            response["code"] = 0
            response["msg"] = "规则不存在"
            self.write(response)
            self.finish()
            return
        response["data"] = detail_info
        self.write(response)
        self.finish()
        return