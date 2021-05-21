<template>
  <div>
    <h1 style="font-size:30px">员工管理</h1>
    <hr style="margin-bottom:15px">
    <div class="sub-header-wrapper">
        <div class="title-comment-wrapper">
            <p style="color:red">* 默认重置密码为：aa123456</p>
        </div>
        <a-button type="primary" @click="showModal">
            新增员工
        </a-button>
        <a-modal
            title="员工详情"
            :visible="visible"
            :disable="editDisabled"
            :confirm-loading="confirmLoading"
            @ok="handleOk"
            @cancel="handleCancel"
        >
            <a-form
                :form="form"    
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
                :disable="editDisabled"
            >
                <a-form-item label="姓名">
                    <a-input
                        v-decorator="[
                            'name', 
                            { rules: [{ required: true, message: '请输入姓名！' }] }
                        ]"
                        v-bind:disabled="editDisabled"
                    />
                </a-form-item>
                <a-form-item label="手机">
                    <a-input
                        v-decorator="['phone_number', { rules: [{ required: true, message: '请输入手机' }] }]"
                        v-bind:disabled="editDisabled"
                    />
                </a-form-item>
                <a-form-item label="部门">
                    <a-select 
                        v-decorator="['department']"
                        placeholder="请选择部门"
                        v-bind:disabled="editDisabled"
                        >
                        <a-select-option value="1">
                            部门1
                        </a-select-option>
                        <a-select-option value="2">
                            部门2
                        </a-select-option>
                        <a-select-option value="3">
                            部门3
                        </a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item label="角色">
                    <a-select
                        v-decorator="['role', {rules: [{required: true, message: '请选择角色！'}]}]"
                        placeholder="请选择角色"
                        v-bind:disabled="editDisabled"
                    >
                        <a-select-option value="1">
                            admin
                        </a-select-option>
                        <a-select-option value="2">
                            角色2
                        </a-select-option>
                        <a-select-option value="3">
                            角色3
                        </a-select-option>
                    </a-select>
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
    <a-table
          :columns="columns"
          :centered=true
          :dataSource="data"
          :rowKey='data=>data.id'
          :pagination="pagination"
          @change="handleTableChange"
          class="data-table"
        >
        <template slot="fileType" slot-scope="text, record">
            <!-- <a>{{text}}</a> -->
            <span v-if="record.fileName.includes('pdf')" style="align:right">
                pdf_log
            </span>
            <span v-else>
                default_log
            </span>
        </template>
        <template slot="operation" slot-scope="text, record">
            <a-dropdown :trigger="['click']">
                <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                    <a-icon type="down"/>
                </a>
                <a-menu slot="overlay">
                    <a-menu-item key="1">
                        <a @click="handleGetAccountInfo(record)">详情</a>
                    </a-menu-item>
                    <a-menu-item key="2">
                        <a @click="handleEditAccountInfo(record)">编辑</a>
                    </a-menu-item>
                    <a-menu-item key="3">
                        <a @click="handleResetPassword(record)">重置密码</a>
                    </a-menu-item>
                    <a-menu-item key="4">
                        <a @click="handleDeleteAccountClick(record)">删除</a>
                    </a-menu-item>
                </a-menu>    
            </a-dropdown>          
        </template>
    </a-table>
  </div>
</template>

<script>
const data = [
    {   
        id: 1,
        name: "测试文件1.pdf",
        phone_number: "2001/02/01",
        department: "111",
        role: "222"
    }
];

const permission = "admin"


const columns = [
    {
    title: "姓名",
    dataIndex: "name",
    align: "center",
    width: 100,
    // scopedSlots: { customRender: "fileType" }
  },
  {
    title: "手机",
    dataIndex: "username",
    align: "center",
    width: 200,
    // scopedSlots: { customRender: "fileType" }
  },
  {
    title: "部门",
    dataIndex: "department",
    align: "center",
    width: 200
  },
  {
    title: "角色",
    dataIndex: "role",
    align: "center",
    width: 200,
  },
  {
    title: "操作",
    align: "center",
    width: 100,
    scopedSlots: { customRender: "operation" }
  }
];
import { createAccount, accountList, resetPasswordDefault, deleteAccount, getAccountInfo, editAccount } from "@/api/user"

export default {
    components: {},
    data() {
        return {
            title: "test",
            columns,
            visible: false,
            saveOrEdit: true, // true：创建账号， false：编辑账号
            editDisabled: false,
            confirmLoading: false,
            form: this.$form.createForm(this, { name: 'coordinated' }),
            labelCol: { span: 5 },
            wrapperCol: { span: 12 },
            data: [], //表格数据显示
            pagination: {}, //分页
            record: {},
            accountInfo: {}, // 账号信息
            editAccountId: "",
        }
    },
    
    // created() {
    //     this.fetchData() //停车场下拉列表
    // },

     mounted() {
        this.queryList() //查询列表
    },
    
    watch: {
    // call again the method if the route changes
        '$route': 'fetchData'
    },

    methods: {
        // 新增员工模块
        showModal() {
            this.visible = true;
        },
        
        handleOk() {
            // 创建账号
            if (!this.editDisabled) {
                if (this.saveOrEdit) {
                    this.handleCreateAccount()
                } else {
                    this.handleEditAccount()
                }
            } else {
                this.handleCancel()
            }
        },

        handleCreateAccount() {
            this.form.validateFields((err, values) => {
                createAccount(values)
                .then(res => {
                    const code = res.code
                    if (code == 1) {
                        this.$message.info("账号创建成功", 1)
                        this.visible = false;
                        this.form.resetFields();
                        this.queryList()
                    } else {
                        this.$message.error(res.msg, 1)    
                    }
                })
                .catch(err => {
                    this.$message.error(err.msg, 1)
                })
            });
        },

        // 取消
        handleCancel(e) {
            this.visible = false;
            this.form.resetFields()
        },

        // -- 人员列表模块
        handleTableChange(pagination) {//表格点击事件
            const pager = { ...this.pagination };
            pager.current = pagination.current;
            this.pagination = pager;
            this.account_list(); //查询列表
        },
        //查询
        queryList() {
            const pager = { ...this.pagination };
            pager.current = 1
            this.pagination = pager;
            this.account_list();
        },
        // 人员接口
        account_list() {
            var parma = {
                page_number: this.pagination.current || 1,
                page_size:10
            };
            accountList(parma)
                .then(res => {
                    if(res.code == '1'){
                        this.data = res.data.content;
                        const pagination = { ...this.pagination };
                        pagination.total = res.data.total_elements;
                        pagination.showTotal = () => `共${pagination.total}条数据`;
                        this.pagination = pagination;
                }})
                .catch(err => {});
        },

        handleClick(title) {
          console.log("clicked", title)
        },
        fetchData() {
          accountList(this.$route.pagination)
            .then(res => {
                const code = res.code
                if (code == 1) {
                    console.log("野马")
                    console.log(this.$route.pagination)
                    this.datahaha = res.data
                    console.log(this.datahaha)
                
                } else {
                    this.$message.error(res.msg, 1)    
                }
          })
          .catch(err => {
              this.$message.error(res.msg, 1)
          })
        },
        getExtension(data) {
          return data
      },
        onSearch(value, event) {
          console.log(value)
      },

        handleChange(info) {
        if (info.file.status !== 'uploading') {
            console.log(info.file, info.fileList);
        }
        if (info.file.status === 'done') {
            this.$message.success(`${info.file.name} file uploaded successfully`);
        } else if (info.file.status === 'error') {
            this.$message.error(`${info.file.name} file upload failed.`);
        }
        },

        // -- 信息详情模块
        // 获取账号信息
        handleGetAccountInfo(record) {
            this.editDisabled = true
            this.saveOrEdit = true
            this.showModal()
            this.form.resetFields();
            const param = {
                "uid": record.id
            }
            getAccountInfo(param)
                .then(response => {
                    this.record = {
                        phone_number: response.data.username,
                        name: response.data.name,
                        role: response.data.role,
                        department: response.data.department
                    }
                    this.$nextTick(() => {  
                        this.form.setFieldsValue(this.record);
                    });
                })
                .catch(error => {
                    this.$message.error(error.msg, 1)

                })
            
        },

        // -- 编辑信息模块
        // 获取账号信息
        handleEditAccountInfo(record) {
            this.handleGetAccountInfo(record)
            this.editDisabled = false
            this.saveOrEdit = false
            this.editAccountId = record.id    
        },

        handleEditAccount() {
            this.form.validateFields((err, values) => {
                const param = {
                    uid: this.editAccountId,
                    name: values.name,
                    phone_number: values.phone_number,
                    department: values.department,
                    position: values.position,
                    role: values.role
                }
                editAccount(param)
                .then(res => {
                    const code = res.code
                    if (code == 1) {
                        this.$message.info("编辑成功", 1)
                        this.visible = false;
                        this.form.resetFields();
                        this.queryList();
                        this.editAccountId = "";
                    } else {
                        this.$message.error(res.msg, 1)    
                    }
                })
                .catch(err => {
                    this.$message.error(err.msg, 1)
                })
            });

        },


        handleDelete() {
            console.log("edit")
        },
        // -- 重置员工密码模块
        // 点击重置
        handleResetPassword(record) {
            const that = this
            this.$confirm({
                title: "提示",
                centered: true,
                okText: "确定",
                cancelText: "取消",
                content: '确认重置？',
            onOk() {
                that.handleResetPasswordConfirm(record); //删除
            },
            onCancel() {
                //that.visible = false;
            }})
        },
        // 执行重置
        handleResetPasswordConfirm(record) {
            const param = {
                "uid": record.id
            }
            resetPasswordDefault(param)
                .then(resp => {
                    if (resp.code == 0) {
                        this.$message.error(resp.msg, 1)
                    } else {
                        this.$message.info("密码重置成功", 1)
                    }  
                })
                .catch(error => {
                    this.$message.error(error.msg, 1)
                })
        },

        // -- 重置员工密码模块
        // 点击重置
        handleDeleteAccountClick(record) {
            const that = this
            this.$confirm({
                title: "提示",
                centered: true,
                okText: "确定",
                cancelText: "取消",
                content: '确定删除该人员',
            onOk() {
                that.handleDeleteAccountExecute(record); //删除
            },
            onCancel() {
                //that.visible = false;
            }})
        },
        // 执行重置
        handleDeleteAccountExecute(record) {
            const param = {
                "uid": record.id
            }
            deleteAccount(param)
                .then(resp => {
                    if (resp.code == 0) {
                        this.$message.error(resp.msg, 1)
                    } else {
                        this.$message.info("人员删除成功", 1)
                        this.queryList()
                    }  
                })
                .catch(error => {
                    this.$message.error(error.msg, 1)
                })
        }

  },
};
</script>
<style>
.sub-header-wrapper {
   line-height: 40px; 
   display: flex;
   justify-content: space-between;
   
}
.title-comment-wrapper {
   line-height: 40px; 
   display: flex;
   justify-content: flex-start;
   
}
.search-box {
    border: none;
    /* vertical-align: middle; */
    display: flex;
    align-items: stretch;
    margin-left: 10px;
    width: 200px;
}
.label {
    font-size: 40px;
    display: flex;
    align-items: stretch;
}
.data-table {
    margin-top: 16px;
}

</style>    
