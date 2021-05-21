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
from .file_apis import *

files_url = [
    # 文件分类操作
    url(r'/files/create_category', CreateCategory, name='创建文件夹分类'),
    url(r'/files/category_list', CategoryList, name='文件分类列表'),

    # 文件夹操作
    url(r'/files/create_folder', CreateFolder, name='创建文件夹'),
    url(r'/files/folder_list', CategorFolderList, name='文件夹列表'),
    url(r'/files/update_category_folder', UpdateCategoryAndFolder, name='更新文件和列表'),

    # 文件操作
    url(r'/files/add_file', UploadFilesOLD, name='上传文件'),
    url(r'/files/upload_files', UploadFiles, name='上传文件'),
    url(r'/files/file_list', FilesList, name='文件列表'),
    url(r'/files/delete_file', DeleteFile, name='删除文件'),
]