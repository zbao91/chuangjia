# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:   __init__.py
    Description:
    Author:      wzj
    Date:        2019/8/6
-------------------------------------------------
    Change Activity:
-------------------------------------------------
"""

from core.application import url
from .standard_apis import *

standard_url = [
    # 目录操作
    url(r'/standard/create_folder', CreateFolder, name='创建目录'),
    url(r'/standard/edit_folder', EditFolder, name='编辑目录名称'),
    url(r'/standard/delete_folder', DeleteFolder, name='删除目录'),
    url(r'/standard/folder_list', FolderList, name='文件分类列表'),

    # 文件操作
    url(r'/standard/file_list', StandardFileList, name='标准列表'),
    url(r'/standard/delete_file', DeleteFile, name='删除文件'),
    url(r'/standard/file_detail', FileDetail, name='文件详情'),
    # url(r'/standard/file_update', FileDetail, name='文件详情'),

    url(r'/standard/create_standard', UploadStandardFile, name='创建标准'),

]