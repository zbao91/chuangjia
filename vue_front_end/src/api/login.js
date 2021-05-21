import {axios} from '@/utils/request'

export function login(parameter) {//登录
  return axios({
    url: 'user/login',
    method: 'post',
    params: parameter
  })
}

export function resetPassword(parameter) {//登录
  return axios({
    url: 'user/reset_password',
    method: 'post',
    params: parameter
  })
}

export function getInfo(parameter) { //用户信息
  return axios({
    url: 'user/authenticate/queryRoleAndMenus',
    method: 'post',
    params: parameter
  })
}

export function logout(parameter) { //退出登录
  return axios({
    url: 'user/logout',
    method: 'post',
    params: parameter
  })
}


export function test() {//登录
  return axios({
    url: 'api/test',
    method: 'get'
  })
}

