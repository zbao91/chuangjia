<template>
  <div class="reset-password">
    <a-form
          id="formLogin"
          class="user-layout-login"
          ref="formLogin"
          :form="form"
        >  
        <div class="flex">
            <div class="input-label-container">
                <label style="position:relative;font-size:20px">旧密码</label>
            </div>
            <div class="input-box-container">
                <a-form-item style="margin-top:10px;width:300px">
                    <a-input-password
                        class="input-box"
                        size="large"
                        placeholder="请输入旧密码"
                        v-decorator="[
                        'old_password',
                        {
                            rules: [{ required: true, message: '不能为空，新重新输入' }],
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
            </div>
        </div>        
        <div class="flex">
            <div class="input-label-container">
                <label style="position:relative;font-size:20px">新密码</label>
            </div>
            <div class="input-box-container">
                <a-form-item style="margin-top:10px;width:300px">
                    <a-input-password
                        class="input-box"
                        size="large"
                        placeholder="请输入新密码"
                        v-decorator="[
                        'new_password1',
                        {
                            rules: [{ required: true, message: '不能为空，新重新输入' }],
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
            </div>
        </div> 
        <div class="flex">
            <div class="input-label-container">
                <label style="position:relative;font-size:20px">确认新密码</label>
            </div>
            <div class="input-box-container">
                <a-form-item style="margin-top:10px;width:300px">
                    <a-input-password
                        class="input-box"
                        size="large"
                        placeholder="请确认新密码"
                        v-decorator="[
                        'new_password2',
                        {
                            rules: [{ required: true, message: '不能为空，新重新输入' }],
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
            </div>
        </div> 
        <a-form-item style="margin-top:13px">
            <a-button
              size="large"
              style="margin-left:115px"
              type="primary"
              class="submit-button"
              @click="handleSubmit"
              >提交</a-button
            >
            <a-button
              size="large"
              type="primary"
              style="margin-left:15px"
              class="reset-button"
              @click="handleResetForm"
              >重置</a-button
            >
        </a-form-item>
    </a-form>
  </div>
</template>

<script>
import Vue from "vue";
import { resetPassword } from '@/api/login'

export default {
  components: {},
  data() {
    return {
        form: this.$form.createForm(this),
        username: Vue.ls.get("username"),
    };
  },

  methods: {
    handleSubmit() { //修改提交
        this.form.validateFields((err, values) => {
            // values.username = username
            values.username = this.username
            resetPassword(values)
            .then(res => {
                this.$message.success('密码重置成功，将自动登出',1)
                Vue.ls.clear()
                this.timer = setTimeout(()=>{   //设置延迟执行
                    this.$router.push("/")
                },1000);
            })
            .catch(err => {
                this.$message.error(err.msg, 1)
            })
        })
        
    },
    handleResetForm() {
        this.form.resetFields()
    }
  }
};
</script>


<style lang="less" scoped>
.reset-password {
    width: 458px;
    margin: auto;
    height: 333px;
    padding-top: 20px;
    }
.flex {
    display: inline-flex;
    height: 50px;
    width: 800px;
    margin-top: 13px;
}
.input-label-container {
    display: flex;
    width: 110px;
    align-items: center;
}
.input-box-container {
    display: flex;
    width: 550px;
    padding-top: 10px;
    align-items: center;
}
</style>
