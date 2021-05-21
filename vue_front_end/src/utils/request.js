import Vue from 'vue'
import axios from 'axios'
import store from '@/store'
import {
  VueAxios
} from './axios'
import notification from 'ant-design-vue/es/notification'
import {
  AUTHORIZATION
} from '@/store/mutation-types'

//const host =  window.location.host  //正式端口80  接口前缀需要https
const host =  `${window.location.host}:8080` //开发端口8080

export const baseURL = 'http://' + (window.location.host.indexOf('localhost') > -1 ? 'localhost:9023' : host)
// 创建 axios 实例
const service = axios.create({
  baseURL: baseURL, // api base_url
  timeout: 600000 // 请求超时时间
})

const err = (error) => {
  if (error.response) {
    const data = error.response.data
    const token = Vue.ls.get(AUTHORIZATION)
    if (error.response.status === 500) {
      notification.error({
        message: '提示',
        description: data.message
      })
    }
    if (error.response.status === 403) {
      // notification.error({
      //   message: 'Forbidden',
      //   description: data.message
      // })
    }
    if (error.response.status === 911) {
      // notification.error({
      //   message: 'Forbidden',
      //   description: data.message
      // })
      if (token) {
        store.dispatch('Logout').then(() => {
          setTimeout(() => {
            window.location.reload()
          }, 500)
        })
      }
    }
    if (error.response.status === 401 && !(data.result && data.result.isLogin)) {
      // notification.error({
      //   message: 'Unauthorized',
      //   description: 'Authorization verification failed'
      // })
      if (token) {
        store.dispatch('Logout').then(() => {
          // setTimeout(() => {
          //   window.location.reload()
          // }, 1500)
        })
      }
    }
  }
  return Promise.reject(error)
}

// request interceptor
service.interceptors.request.use(config => {
  const token = Vue.ls.get(AUTHORIZATION)
  const role = Vue.ls.get("role")
  // const organizeId = Vue.ls.get('organizeId')
  // const organizeUnionId = Vue.ls.get('organizeUnionId')
  if (token) {
    config.headers['Authorization'] = token // 让每个请求携带自定义 token 请根据实际情况自行修改
    config.headers['role'] = role
    //config.headers['organizeId'] = organizeId
    if(config.url.indexOf('getPersonInfoByIdNumber')>-1||config.url.indexOf('getAlarmModelInfo')>-1||config.url.indexOf('getLastestSms')>-1||config.url.indexOf('getAlarmSnapshotImage')>-1){
      config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    }else{
      config.headers['Content-Type'] = 'application/json'
    }
    // config.headers['belongToOrganizeUnionId'] = organizeId
    // config.headers['organizeUnionId'] = organizeUnionId
  }
  return config
}, err)

// response interceptor
service.interceptors.response.use((response) => {
  return response.data
}, err)

const installer = {
  vm: {},
  install(Vue) {
    Vue.use(VueAxios, service)
  }
}

export {
  installer as VueAxios,
  service as axios
}
