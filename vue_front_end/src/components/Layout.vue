<template>
  <a-layout id="components-layout-demo-custom-trigger">
    <a-layout>
      <a-layout-header>
        <div class="header-content">
          <div class="header-content-list">
            <!-- <img src="../assets/imgs/icon_logo.png"  style="width:50px;"/>   -->
            <span style="font-size: 27px;font-family: HYk2gj;"> 创佳</span>
            <!-- <a-select
              class="serch-item-input"
              v-model="deptIds"
            >
                <a-select-option  v-for="key in organizationlist" :key="key.id">
                  {{ key.deptName }}
                </a-select-option>
            </a-select> -->
          </div>
          <div>
            <span style="margin-right:1px;;color:rgba(255, 255, 255, 0.6)">{{name}}</span>
            <a-dropdown class="user">
            <a style="color: rgba(255, 255, 255, 0.6);;margin-left:10px;" class="ant-dropdown-link" @click="e => e.preventDefault()">
              <img style="width:35px;margin-right:5px;" :src="userlogo" alt="" />{{USERNAME_NAME}}<a-icon type="down" />
            </a>
            <a-menu slot="overlay">
              <a-menu-item v-if="user_role.includes('admin')" key="1" @click="handleUserManager">
                <a-icon type="user"/>
                <span>用户管理中心</span>
              </a-menu-item>
              <a-menu-item key="2" @click="handleResetPassword">
                <a-icon type="setting"/>
                <span>修改密码</span>
              </a-menu-item>
              <a-menu-item key="3" @click="handleLogout ">
                <a-icon type="logout"/>
                <span>退出登录</span>
              </a-menu-item>
            </a-menu>
            </a-dropdown>
          </div>
        </div>
      </a-layout-header>
        <a-layout class="contentbox">
          <a-layout-sider class="sider" v-model="collapsed" :trigger="null" collapsible>
            <a-menu mode="inline" 
              theme="dark" 
              :selectedKeys="selectedKeys"
              :openKeys.sync="openKeys"
              >
              <template v-for="item in menu">
                <sub-menu v-if="item.children.length>0" :menu-info="item" :key="item.path" />
                <a-menu-item :key="item.path" v-else >
                  <router-link :to="item.path">
                    <a-icon :type="item.type" />
                    <span>{{item.text}}</span>
                  </router-link>
                </a-menu-item>
              </template>
            </a-menu>
          </a-layout-sider>
        <a-layout-content :style="{ padding: '24px'}">
          <router-view/>
        </a-layout-content>
        </a-layout>
    </a-layout>
  </a-layout>
</template>

<script>
import Vue from 'vue'
import { mapState } from 'vuex'
import SubMenu from "./SubMenu";
import userlogo from '@/assets/imgs/user_logo.png'
export default {
  data() {
    this.selectedKeysMap = {};
    this.openKeysMap = {};
    const menuData = this.getMenuData(this.$store.state.user.menu);
    return {
      name: Vue.ls.get("name") ? Vue.ls.get("name"): "默认用户",
      userlogo,
      deptIds:"1",
      // organizationlist:[{id:"1",deptName:"哈哈说"}],//左上角下拉列表
      collapsed: false,
      rootSubmenuKeys: [],
      // selectedKeys:[this.$route.path],
      // openKeys:[],
      selectedKeys: this.selectedKeysMap[this.$route.path],
      openKeys: this.openKeysMap[this.$route.path],
      user_role: "admin"
    };
  },
  components: {
    "sub-menu": SubMenu
  },
  computed: {
    ...mapState({
      // 动态主路由
      menu: state => state.user.menu
    }),
  },
    watch: {
    "$route.path": function(val) {
      this.selectedKeys = this.selectedKeysMap[val];
      this.openKeys =this.openKeysMap[val];
    }
  },
  
  methods: {
    handleLogout (e) { //退出
      this.$Modal.confirm({
        title: "提示",
        content: "是否退出？",
        onOk: () => {
          return this.$store.dispatch('Logout').then(() => {
            this.$message.success('登出成功！',1)
            this.$router.push('/login')
          })
        },
        onCancel () {}
      })
    },

    getMenuData(routes = [], parentKeys = [], selectedKey) {
      const menuData = [];
      for (let item of routes) {
        // if (item.meta && item.meta.authority && !check(item.meta.authority)) {
        //   break;
        // }
        if (item.name) {
          this.openKeysMap[item.path] = parentKeys;
          this.selectedKeysMap[item.path] = [selectedKey || item.path];
          const newItem = { ...item };
          delete newItem.children;
          if (item.children) {
            newItem.children = this.getMenuData(item.children, [
              ...parentKeys,
              item.path
            ]);
          } else {
            this.getMenuData(
              item.children,
              selectedKey ? parentKeys : [...parentKeys, item.path],
              selectedKey || item.path
            );
          }
          menuData.push(newItem);
        } else if (
          !item.hideInMenu &&
          !item.hideChildrenInMenu &&
          item.children
        ) {
          menuData.push(
            ...this.getMenuData(item.children, [...parentKeys, item.path])
          );
        }
      }
      return menuData;
    },

    handleResetPassword (e) {
      this.$router.push('/ResetPassword')
    },

    handleUserManager (e) {
      this.$router.push('/UserManager')
    }
  },
};
</script>

<style lang="less" scoped>
#components-layout-demo-custom-trigger {
  .header-content{
    color: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    .header-content-list{
      display: flex;
      align-items: center;
      .serch-item-input{
        width:"118px";
        margin-left: 35px;
        &/deep/ .ant-select-selection--single{
          background: #001529;
          color: rgba(255, 255, 255, 0.6);
          border: none;
        }
        &/deep/ .ant-select-arrow-icon {
          color: rgba(255, 255, 255, 0.6);
        }
        &/deep/ .ant-select-open{
          & /deep/.ant-select-selection{
            border:none!important;
          }
        }
      }
    }
  }
  .trigger {
    font-size: 18px;
    line-height: 64px;
    padding: 0 24px;
    cursor: pointer;
    transition: color 0.3s;
  }
  .trigger:hover {
    color: #1890ff;
  }
  .logo {
    height: 32px;
    background: rgba(255, 255, 255, 0.2);
    margin: 16px;
  }
  .contentbox{
    height: calc(100vh - 11px);
    display: flex;
  }

}
@import "../assets/styles/global.less";
</style>
