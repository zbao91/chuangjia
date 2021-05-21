<template>
  <div class="login">
    <div class="loginbox">
      <div class="title">
        <span class="title_logo">创佳内部管理系统</span>
      </div>
      <div class="main">
        <a-form
          id="formLogin"
          class="user-layout-login"
          ref="formLogin"
          :form="form"
        >
          <a-form-item>
            <a-input
              class="loginname"
              size="large"
              type="text"
              placeholder="请输入帐户"
              v-decorator="[
                'username',
                {
                  rules: [{ required: true, message: '请输入帐户名' }],
                  validateTrigger: 'blur'
                }
              ]"
            >
              <a-icon
                slot="prefix"
                type="user"
                :style="{fontSize: '20px',marginRight:'15px', color: 'rgba(255,255,255,0.78)' }"
              />
            </a-input>
          </a-form-item>
          <a-form-item>
            <a-input-password
              class="password"
              size="large"
              placeholder="请输入密码"
              v-decorator="[
                'password',
                {
                  rules: [{ required: true, message: '请输入密码' }],
                  validateTrigger: 'blur'
                }
              ]"
              autocomplete
            >
              <a-icon
                slot="prefix"
                type="lock"
                :style="{fontSize: '20px',marginRight:'15px', color: 'rgba(255,255,255,0.78)' }"
              />
            </a-input-password>
          </a-form-item>
          <a-form-item style="margin-top:24px">
            <a-button
              size="large"
              type="primary"
              class="login-button"
              @click="handleSubmit"
              >登录</a-button
            >
          </a-form-item>
        </a-form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import Vue from 'vue'
import {randomWord} from '@/utils/util'
export default {
  name: "Login",
  data() {
    return {
      form: this.$form.createForm(this),
    };
  },
  methods: {
    ...mapActions(["Login", "Logout"]),
    handleSubmit(){ //登录提交
      const { Login } = this;
      this.form.validateFields((errors, values) => {
        const record = { 
          ...values
        }
        if (!errors) {
          Login(record)          
          .then(res => this.loginSuccess(res))
            .catch(err => this.requestFailed(err))
        }
      })

    },
    loginSuccess(res) {
      if(res.data){
         this.$message.success('登录成功！',1)
          setTimeout(()=>{
            this.$router.push("/").catch(()=>{});
          },1000)
      }
    },
    requestFailed(err) {
      if (err.code != 1) {
        this.$message.warning(err.msg,3)
      }
    },
  }
};
</script>

<style lang="less" scoped>
/deep/ input:-webkit-autofill,
/deep/ input:-webkit-autofill:hover,
/deep/ input:-webkit-autofill:focus,
/deep/ input:-webkit-autofill:active {
  //通过延长增加自动填充背景色的方式, 是用户感受不到样式的变化
  transition-delay: 99999s;
  transition: color 99999s ease-out, background-color 99999s ease-out;
}
.login {
    width: 100%;
    height: 100vh;
    background: #f0f2f5 url(../../assets/imgs/bg.png) no-repeat 100%;
    padding: 252px 0 144px;
    position: relative;
    color: black;
    .loginbox{
      width: 458px;
      margin: auto;
      height: 333px;
      padding-top: 20px;
      background: rgba(20,58,98,0.70);
      border: 1px solid rgba(255,255,255,0.2);
      box-shadow: -1px 1px 37px 8px rgba(0,0,0,0.22);
      border-radius: 5px;
      border-radius: 5px;
      .title {
        height: 75px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 15px;
        .logo{
          width: 50px;
        }
        .title_logo{
          font-size: 27px;
          color:#fff;
          font-family: HYk2gj;
        }
    }
  }
  .main {
    min-width: 260px;
    width: 368px;
    margin: 0 auto;
    /deep/.ant-input{
      background: #133359;
      border: 1px solid rgba(0,0,0,0.1);
      border-radius: 4px;
      color:rgba(255,255,255,0.68);
      letter-spacing: 0;
      padding-left: 40px;
    }
    /deep/.ant-input-password-icon{
      color:rgba(255,255,255,0.78);
    }
  }
  .user-layout-login {
    label {
      font-size: 14px;
    }

    .getCaptcha {
      display: block;
      width: 100%;
      height: 40px;
    }

    .forge-password {
      font-size: 14px;
    }

    button.login-button {
      padding: 0 15px;
      font-size: 16px;
      height: 40px;
      width: 100%;
      background: #00C0FF;
      border-radius: 4px;
      border-radius: 4px;
      margin-top: 15px;
    }

    .user-login-other {
      text-align: left;
      margin-top: 24px;
      line-height: 22px;

      .item-icon {
        font-size: 24px;
        color: rgba(0, 0, 0, 0.2);
        margin-left: 16px;
        vertical-align: middle;
        cursor: pointer;
        transition: color 0.3s;

        &:hover {
          color: #1890ff;
        }
      }

      .register {
        float: right;
      }
    }
  }
}
</style>
