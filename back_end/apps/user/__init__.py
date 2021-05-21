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
from .user_apis import *

user_url = [
    url(r'/user/login', Login, name='登陆接口'),
    url(r'/user/logout', Logout, name='登出接口'),
    url(r'/user/reset_password', ResetPassword, name='重置密码'),
    url(r'/user/create_account', CreateAccount, name='创建账号'),
    url(r'/user/account_list', AccountList, name='账号列表'),
    url(r'/user/reset_password_default', RestPasswordDefault, name='默认重置密码为：aa123456'),
    url(r'/user/delete_account', DeleteAccount, name='删除用户'),
    url(r'/user/account_info', AccountInfo, name='用户信息'),
    url(r'/user/edit_account', EditAccount, name='编辑用户信息'),

    # 测试
    url(r'/user/create_account_tmp', CreateAccountTmp, name='创建临时账号'),


]