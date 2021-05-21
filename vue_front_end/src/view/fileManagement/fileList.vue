<template>
  <div>
    <div class="search-box-wrapper">
        <label style="font-size:30px" class="label">{{folderName}}</label>
        <div class="search-box-upload-btn-wrapper">
            <a-upload
                name="file"
                :multiple="true"
                :action="url.upload"
                :headers="headers"
                :before-upload="beforeUpload"
                :data="{'folder_id':folderId, 'file_name': uploadedFileName}"
                :showUploadList="false"
                @change="handleChange"
            >
                <a-button> <a-icon type="upload" /> 点击上传 </a-button>
            </a-upload>
            <a-input-search 
                style="margin-top:5px"
                class="search-box"
                placeholder="请输入文件名称" 
                v-model="searchKeyword"
                enter-button 
                allowClear
                @search="onSearch"/>
            <a-button type="primary" style="margin-left: 10px; margin-top:5px" @click="handleReset">重置</a-button>
        </div>
    </div>
    <a-table
          :columns="columns"
          :dataSource="fileList"
          :rowKey='fileList=>fileList.file_id'
          :pagination="pagination"
          class="data-table"
          @change="handleTableChange"
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
            <div >
              <!-- <a class="tool-table" @click="go()">测试详情</a> -->
                <!-- <img :src="record.file_path" :id="record.file_id">
                <input type="button" id="btnsavaImg" value="保存图片到本地" @click="downloadIamge(record.file_id,record.file_path)"/>    -->

              <!-- <a @click="downloadIamge(record)" >下载</a> -->
              <a :href="record.file_path" :download="record.file_name" target="_blank">下载</a>
              <a  @click="handleDelete(record)">刪除</a>
            </div>
        </template>
        <!-- <span slot="customTitle"><a-icon type="smile-o" /> Name</span> -->
    </a-table>
  </div>
</template>

<script>
const permission = "admin"
const columns = [
    {
    title: "文件类型",
    dataIndex: "file_type",
    align: "center",
    width: 100,
    scopedSlots: { customRender: "file_type" }
  },
  {
    title: "文件名称",
    dataIndex: "file_name",
    align: "center",
    width: 300
  },
  {
    title: "上传时间",
    dataIndex: "create_time",
    align: "center",
    width: 200,
    sorter: true,
  },
  {
    title: "操作",
    dataIndex: "dataOperation",
    align: "center",
    width: 100,
    scopedSlots: { customRender: "operation" }
  }
];

import Vue from 'vue';
import { refs } from 'vue';
import { getFileList, uploadFiles, deleteFile, createFileRecord } from '@/api/filesManager'
export default {
    components: {},
    data() {
        return {
            searchKeyword: null,
            fileList: [],
            folderName: "",
            uploadedFileName: "",
            folderId: "",
            columns,
            pagination: {
                total: 0,
                pageSize: 10,//每页中显示10条数据
                // showSizeChanger: true,
                pageSizeOptions: ["10", "20", "50", "100"],//每页中显示的数据
                showTotal: total => `共有 ${total} 条数据`,  //分页中显示总的数据
            }, //分页
            permission: permission,
            headers: {
            },
            url: {
                upload: "http://localhost:9023/files/upload_files", //上传图片
            },
        }
    },
    
    created() {
        // this.queryFiles() //停车场下拉列表
    },

    mounted() {
        this.queryFiles({}) //停车场下拉列表
    },
    
    watch: {
    // call again the method if the route changes
        '$route': 'queryFiles'
    },

    methods: {
        handleTableChange(pagination, filters, sorter) {//表格点击事件
            const pager = { ...this.pagination };
            pager.current = pagination.current;
            this.pagination = pager;
            const param = {
                sort_field: sorter.field,
                sort_order: sorter.order,
                keyword: "",
            }
            
            this.queryFiles(param); //查询列表
        },
        queryFiles(input) {
            this.folderName = Vue.ls.get("CurrentFolder")
            this.folderId = Vue.ls.get("CurrentFolderId")
            const pager = { ...this.pagination };
            pager.current = 1
            this.pagination = pager;
            var param = {...input}
            param.page_number = this.pagination.current || 1,
            param.page_size = 10
            param.folder_id = this.folderId
            getFileList(param)
                .then(res => {
                    if(res.code == '1'){
                        this.fileList = res.data.content;
                        const pagination = { ...this.pagination };
                        pagination.total = res.data.total_elements;
                        pagination.showTotal = () => `共${pagination.total}条数据`;
                        this.pagination = pagination;
                }})
                .catch(err => {});
        },

        handleReset(){
            const pager = { ...this.pagination };
            pager.current = 1
            this.pagination = pager;
            this.$nextTick().then(() => {
            this.queryFiles({
                sort_field: "",
                sort_order: "",
                keyword: "",
            }
            )
            this.searchKeyword = null
            })
        },
    
        handleClick(title) {
            console.log("clicked", title)
        },
        fetchData() {
            console.log("请求参数", this.$route.params)
        },
        getExtension(data) {
            return data
        },
        onSearch(value) {
            this.queryFiles({
                sort_field: "",
                sort_order: "",
                keyword: value,
            })
        },

        beforeUpload(file) {
            const isLt10M = file.size / 1024 / 1024 < 10;
            this.uploadedFileName = file.name
            if (!isLt10M) {
                this.$message.error('上传的文件需小于 10MB!');
            }
            
            return isLt10M;
        },

        handleChange(info) {
            const status = info.file.status
            if (status === 'done') {
                this.$message.success('文件上传成功...', 2)
                const uploaded_file_path = info.file.response.data.file_path
                const uploaded_file_uuid = info.file.response.data.uid
                const file_name = info.file.response.data.file_name
                const param = {
                    folder_id: this.folderId,
                    file_name: this.file_name,
                    file_path: uploaded_file_path,
                    file_uid: uploaded_file_uuid,
                    file_name: file_name
                }
                createFileRecord(param) 
                    .then(resp => {})
                    .catch(err => {})
                this.queryFiles({})
                
            } else if (status === 'error') {
                this.$message.error(`${info.file.name} 文件上传失败`)
            }
        },
        
        handleDelete(record) {
            const param = {
                file_id: record.file_id
            }
            const that = this
            this.$confirm({
                title: "提示",
                centered: true,
                okText: "确定",
                cancelText: "取消",
                content: '确认删除？',
                onOk() {
                    deleteFile(param)
                        .then(resp => {
                            if (resp.code == 1) {
                                that.$message.info("删除成功", 1)
                                that.queryFiles({
                                    sort_field: "",
                                    sort_order: "",
                                    keyword: "",
                                })
                                
                            } else {
                                that.$message.error(res.msg, 1)
                                that.form.resetFields()
                            }
                        })
                        .catch(err => {})
                    
                },
                onCancel() {
            }
            })
        },

        handleDownload(record) {
            let a = document.createElement('a')
            a.href = record.file_path // 这里的请求方式为get，如果需要认证，接口上需要带上token
            a.click()
        },
  },
};
</script>
<style>
.search-box-wrapper {
   line-height: 40px; 
   display: flex;
   justify-content: space-between;
   
}
.search-box-upload-btn-wrapper {
   line-height: 40px; 
   display: flex;
   justify-content: space-between;
   
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
