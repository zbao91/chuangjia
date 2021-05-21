import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'
import {AUTHORIZATION} from '@/store/mutation-types'
import notification from 'ant-design-vue/es/notification'
import createRoutes from '@/utils/createRoutes'

Vue.use(Router)

/**
  路由
* */
export const commonRoutes =
  [
    {
      path: "/login",
      name:"login",
      component: () => import("@/view/login/login")
    },
    {
      path: '/404',
      name:'404',
      meta: { title: '404' },
      component: () => import('../components/404.vue'),
    }
  ];
// 本地所有的页面 需要配合后台返回的数据生成页面
export const asyncRoutes = {
  categoryList: {
    path: '/categoryList',
    name: 'categoryList',
    meta: { title: '文件夹列表' },
    component: () => import('@/view/fileManagement/categoryFolderList.vue'),
  },
  StandardList: {
    path: '/StandardManagement',
    name: 'StandardManagement',
    meta: { title: '标准管理' },
    component: () => import('@/view/standardManagement/categoryFolderList.vue'),
  },
  ImageManagement: {
    path: '/ImageManagement',
    name: 'ImageManagement',
    meta: { title: '图号管理' },
    component: () => import('@/view/imageManagement/ImageList.vue'),
  },
}
const createRouter = () =>new Router({
  scrollBehavior: () => ({ x: 0, y: 0 }),
  routes: commonRoutes
})
const router = createRouter()

export function resetRouter() { //重置路由
  const newRouter = createRouter()
  router.matcher = newRouter.matcher
}

// 是否有菜单数据
let hasMenus = false

router.beforeEach((to, from, next) => {
  const token=Vue.ls.get(AUTHORIZATION)
  if (token) {
      if (to.path === '/login') {
          next({ path: '/' })
      } else if (hasMenus) {
          next()
      } else {
          try {
            const ismenu=JSON.parse(Vue.ls.get('menu'))
            let menu=[]
            if(ismenu){
              menu=ismenu
              store.state.user.menu=menu //给state赋值
            }else{
              menu=store.state.user.menu
            }
              // 这里可以用 await 配合请求后台数据来生成路由
              // const data = await axios.get('xxx')
              // const routes = createRoutes(data)
            const routes = commonRoutes.concat(createRoutes(menu))
            router.options.routes = routes
            // 动态添加路由
            router.addRoutes(routes)
            hasMenus = true
            if(to.path=="/"){
              next({ path:routes[2].children[0].path})
            }else{
              next({ path:to.path })
            }
            
          } catch (error) {
              resetRouter()
              next(`/login`)
          }
      }
  } else {
      hasMenus = false
      if (to.path === '/login') {
          next()
      } else {
          notification.error({
            message: '提示',
            description: "您未登录，请登录！"
          })
          next(`/login`)
      }
  }
})


export default router

