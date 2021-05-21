from core.application import url
from .image_management_apis import *

image_url = [
    # 文件分类操作
    url(r'/images/image_apply', ApplyImage, name='图号申请'),
    url(r'/images/image_applications', ImageApplicationList, name='图号申请列表'),
    url(r'/images/image_application_pass', ImageApplicationPass, name='图号申请审核通过'),
    url(r'/images/image_application_deny', ImageApplicationDeny, name='图号申请审核通过'),
    url(r'/images/image_list', ImageList, name='图号列表'),


    # 规则
    url(r'/images/image_add_rule', AddImageRule, name='图号规则新增'),
    url(r'/images/image_rule_list', ImageRuleList, name='图号规则列表'),
    url(r'/images/image_delete_rule', DeleteImageRule, name='图号规则列表'),
    url(r'/images/image_rule_detail', ImageRuleDetails, name='图号规则列表'),
    url(r'/images/search_rule', SearchRule, name='图号规则搜索'),
    url(r'/images/rule_detail', RuleDetail, name='规则详情'),

    # 删除图号
    url(r'/images/image_delete', DeleteImage, name='删除图号'),
    url(r'/images/image_detail', ImageDetail, name='图号详情'),
]