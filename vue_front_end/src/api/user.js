import {axios} from '@/utils/request'

export function createAccount(parameter) {//创建账号
  return axios({
    url: 'user/create_account',
    method: 'post',
    params: parameter
  })
}

export function accountList(parameter) {//获取账号列表
  return axios({
    url: 'user/account_list',
    method: 'get',
    params: parameter
  })
}

export function resetPasswordDefault(parameter) {//默认重置密码为：aa123456
  return axios({
    url: 'user/reset_password_default',
    method: 'post',
    params: parameter
  })
}

export function deleteAccount(parameter) {//删除账号
  return axios({
    url: 'user/delete_account',
    method: 'post',
    params: parameter
  })
}

export function getAccountInfo(parameter) {//账号信息
  return axios({
    url: 'user/account_info',
    method: 'get',
    params: parameter
  })
}

export function editAccount(parameter) {//账号信息
  return axios({
    url: 'user/edit_account',
    method: 'post',
    params: parameter
  })
}