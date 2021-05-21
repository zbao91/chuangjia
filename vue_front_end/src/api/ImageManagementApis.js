import {axios} from '@/utils/request'

export function ImageApply(parameter) {// 申请图号
    return axios({
      url: 'images/image_apply',
      method: 'post',
      params: parameter
    })
  }

export function ImageApplications(parameter) {// 图号申请列表
  return axios({
    url: 'images/image_applications',
    method: 'get',
    params: parameter
  })
}

export function ImageApplicationPass(parameter) {// 申请通过
  return axios({
    url: 'images/image_application_pass',
    method: 'post',
    params: parameter
  })
}

export function ImageApplicationDeny(parameter) {// 申请不通过
  return axios({
    url: 'images/image_application_deny',
    method: 'post',
    params: parameter
  })
}


export function ImageList(parameter) {// 图号列表
  return axios({
    url: 'images/image_list',
    method: 'get',
    params: parameter
  })
}

export function AddImageRule(parameter) {// 申请图号
  return axios({
    url: 'images/image_add_rule',
    method: 'post',
    params: parameter
  })
}

export function ImageRuleList(parameter) {// 图号规则列表
  return axios({
    url: 'images/image_rule_list',
    method: 'get',
    params: parameter
  })
}

export function DeleteImageRule(parameter) {// 删除图号规则
  return axios({
    url: 'images/image_delete_rule',
    method: 'post',
    params: parameter
  })
}

export function SearchRule(parameter) {// 删除图号规则
  return axios({
    url: 'images/search_rule',
    method: 'get',
    params: parameter
  })
}


export function ImageDetail(parameter) {// 删除图号规则
  return axios({
    url: 'images/image_detail',
    method: 'get',
    params: parameter
  })
}

export function ImageDelete(parameter) {// 删除图号
  return axios({
    url: 'images/image_delete',
    method: 'post',
    params: parameter
  })
}

export function RuleDetail(parameter) {// 规则详情
  return axios({
    url: 'images/rule_detail',
    method: 'get',
    params: parameter
  })
}