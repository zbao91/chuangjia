import { asyncRoutes } from '@/router'

// 将菜单信息转成对应的路由信息 动态添加
export default function createRoutes(data) {
    const result = []
    const children = []
    result.push({
        path: '/',
        component: () => import('../components/Layout.vue'),
        children: children
    })

    data.forEach(item => {
        generateRoutes(children, item)
    })

    // 最后添加404页面 否则会在登陆成功后跳到404页面
    result.push(
        { path: '*', redirect: '/404' },
    )
    children.push({
        path: '/ResetPassword',
        name:'ResetPassword',
        meta: { title: '重置密码' },
        component: () => import('@/view/user/ResetPassword.vue'),
      })
    children.push({
        path: '/fileList',
        name: 'fileList',
        meta: { title: '文件列表' },
        component: () => import('@/view/fileManagement/fileList.vue'),
    })
    children.push({
        path: '/UserManager',
        name: 'UserManager',
        meta: { title: '用户管理' },
        component: () => import('@/view/user/UserManager.vue'),
    })
    return result
}

function generateRoutes(children, item) {
    if (item.name) {
        if (asyncRoutes[item.name]) children.push(asyncRoutes[item.name])
    } else if (item.children) {
        item.children.forEach(e => {
            generateRoutes(children, e)
        })
    }
}