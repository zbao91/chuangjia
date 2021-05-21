# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   sql
    Description: 
    Author:      wzj
    Date:        2019/8/2
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

import re
import numbers


class SqlHandlers:

    def __init__(self):
        """Constructor"""
        __ulei__ = "xulei"

    def _setDb(self, db):
        """"""
        self.db = db

    def _select(self, table_name, keyList, **kwargs):
        """
        table_name: 表名
        keyList: 查询字段列表
        kwargs: 条件参数
        """
        keys = ",".join(keyList)
        sql = "SELECT %s FROM `%s`" % (keys, table_name)
        getSql, rparam = self.__buildSql(sql, **kwargs)
        return getSql, rparam

    def _insert(self, table_name, keyDict:dict):
        """
        table_name: 表名
        keyDict: 参数字典
        kwargs: 条件参数
        """
        keys, values = [], []
        rparam = {}
        for key, value in keyDict.items():
            keys.append('`%s`' % key)
            if isinstance(value, numbers.Number):
                values.append(str(value))
            elif value in ['now()', 'NOW()']:
                values.append(value)
            else:
                values.append("'{%s}'" % key)
                rparam[key] = value
        keys = ",".join(keys)
        values = ','.join(values)
        sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (table_name, keys, values)
        return sql, rparam

    def _update(self, table_name, keyDict, **kwargs):
        """
        更新语句重组
        table_name: 表名
        keyDict: 参数字典
        kwargs: 条件参数
        """
        setList, uparam = self._setUpdateParam(keyDict)
        if not setList:
            raise Exception('不存在更新操作')
        setData = ",".join(setList)
        sql = "UPDATE %s SET %s" % (table_name, setData)
        getSql, wparam = self.__buildSql(sql, **kwargs)
        uparam.update(wparam)
        getSql
        return getSql.format(**uparam)

    def _setUpdateParam(self, keyDict):
        sqlList = []
        rparam = {}
        for key, value in keyDict.items():
            if type(value) in [int, float]  :
                data = "`%s`=%s" % (key, value)
            elif value in ["now()", "NOW()"]:
                data = "`%s`=%s" % (key, value)
            else:
                data = "%s='%s'" % (key, '{u_%s}' % key)
                rparam['u_%s' % key] = value
            sqlList.append(data)
        return sqlList, rparam

    def sqlfix(self, sql):
        """
        转义特殊字符
        参数绑定 数据库进行转义
        """
        sql = re.sub(r"(?<!%)%(?!%)", "%%", sql)
        #sql = re.sub(r"(?<!')'(?!')", r"''", sql)
        sql = re.sub(r"(?<!\\)\\(?!\\)", r"\\\\", sql)
        return sql

    def where(self, params):
        """
        where条件:
        params: [(key, value, way, mode),(key, value, way, mode),...]
        way: "=", "!=", "like"
        mode: "and", "or"
        """
        rparam = {}
        whereList = ["where"]
        for param in params:
            key, value, way, mode = param
            if way == 'like':
                raise Exception('不支持like方法')
            if way == "in":
                if isinstance(value, (list, tuple)):
                    value_s = [str(item) for item in value]
                    if any(map(lambda i: isinstance(value[0], str), value)):
                        # 有任何一个字符类型
                        in_where = "('" + "','".join(value) + "')"
                    else:
                        in_where = "(" + ','.join(value_s) + ")"
                else:
                    in_where = value
                data = "`%s` in %s" % (key, '{%s}' % key)
                rparam[key] = in_where
            else:
                if type(value) == int:
                    data = "`%s` %s %s" % (key, way, value)
                else:
                    data = "`%s` %s '%s'" % (key, way, '{%s}' % key)
                    rparam[key] = value
            if mode:
                data += " %s" % mode
            whereList.append(data)
        setWhere = " ".join(whereList)
        if setWhere.endswith(('and', 'or', 'AND', 'OR')):
            rindex = setWhere.rindex(' ')
            setWhere = setWhere[:rindex or len(setWhere)]
        return setWhere, rparam

    #----------------------------------------------------------------------
    def __order(self, params):
        """
        降序与升序
        params: [(key, desc), (kes2, asc)...]
        key: 表示数据库字段
        """
        if isinstance(params, str):
            return params
        if isinstance(params[0], str):
            return ' '.join(params)
        if isinstance(params[0], (list, tuple)):
            setList = []
            for param in params:
                setList.append(" ".join(param))
            return ",".join(setList)

    #----------------------------------------------------------------------
    def __buildSql(self, sql, **kwargs):
        """
        {
           "where":__where,
           "limit": "__limit",
           "order": "__order",
        }
        """
        rparam = {}
        if 'where' in kwargs:
            where_sql, rparam = self.where(kwargs["where"])
            sql = "%s %s" % (sql, where_sql)
        if 'order' in kwargs:
            order = "ORDER BY %s" % self.__order(kwargs["order"])
            sql = "%s %s" % (sql, order)
        if 'limit' in kwargs:
            limits = "LIMIT %d, %d" % (kwargs["limit"][0], kwargs['limit'][1])
            sql = "%s %s" % (sql, limits)
        return sql, rparam
