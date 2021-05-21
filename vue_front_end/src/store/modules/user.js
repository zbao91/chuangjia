/* eslint-disable */
import Vue from 'vue'
import { resetRouter } from '@/router'
import { login, logout } from '@/api/login'
import {AUTHORIZATION} from '@/store/mutation-types'
const user = {
  state: {
    communityCode:'111',//社区编号默认写死的编号
    token: '',
    menu:[],
  },

  mutations: {
    SET_TOKEN: (state, userInfo) => {
      state.token = userInfo.token
      state.menu=[...userInfo.menu]
    }
  },

  actions: {
    // 登录
      Login({commit}, userInfo) {
        return new Promise((resolve, reject) => {
          login(userInfo).then(response => {
            if (response.data) {
              const token = response.data.token
              const role = response.data.role
              const username = response.data.username
              const name = response.data.name
              const menu=[
                {
                  text: "文件管理",
                  type: "menu",
                  path: "/categoryList",
                  name: "categoryList",
                  children: []
                },
                {
                  text: "标准管理",
                  type: "menu",
                  name: "StandardList",
                  path: "/StandardManagement",
                  children: [
                  ]
                },
                {
                  text: "图号管理",
                  type: "menu",
                  path: "/ImageManagement",
                  name: "ImageManagement",
                  children: [
                  ]
                },
              ]
              Vue.ls.set('menu',JSON.stringify(menu), 7* 24 * 60 * 60 * 1000) ////有效1小时
              const userInfo={
                token: token,
                menu: menu,
              }
              commit('SET_TOKEN', userInfo) //提交用户信息
              Vue.ls.set(AUTHORIZATION, token, 7 * 24 * 60 * 60 * 1000)
              Vue.ls.set("role", role, 7 * 24 * 60 * 60 * 1000)
              Vue.ls.set("username", username, 7 * 24 * 60 * 60 * 1000)
              Vue.ls.set("name", name, 7 * 24 * 60 * 60 * 1000)
              resolve(response)
  
            } else {
              reject(response)
            }
          }).catch(error => {
            reject(error)
          })
        })
      },
    // 登出
    Logout ({ commit }) {
      return new Promise((resolve) => {
        const parm={token:Vue.ls.get(AUTHORIZATION), username: Vue.ls.get("username")}
        logout(parm).then(() => {
          commit('SET_TOKEN', {'token':"",'menu':[]})
          Vue.ls.clear(); //清楚本地缓存
          resetRouter() //重置路由
          resolve()
        }).catch(() => {
          resolve()
        }).finally(() => {
        })
      })
    }

  }
}

export default user
