<template>
    <div class="folder-wrapper">
        <div class="header-container">
            <h1 style="font-size:30px">标准管理</h1>
            <div :trigger="['click']">
                        <a-dropdown>
                            <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                                <a-button @click="showAddFolder" type="primary">标准目录创建</a-button>
                                <a-button @click="showFolderManage" type="primary">标准目录管理</a-button>
                                <a-button @click="showUploadFile" type="primary">标准录入</a-button>
                            </a>
                        </a-dropdown>
            </div>
        </div>
        <a-modal
            :visible="addFolderVisible"
            :confirm-loading="confirmLoading"
            @ok="handleAddFolderOk"
            @cancel="handleAddFolderCancel"
        >   
            <div>
                <!-- 创建目录 -->
                <a-radio-group v-model="addCategoryOrFolder" default-value=1 button-style="solid" @change="onChange">
                    <a-radio-button value=1>
                        新增目录
                    </a-radio-button>
                    <a-radio-button value=2>
                        新增子目录
                    </a-radio-button>
                </a-radio-group>
            </div>
            <hr>
            <a-form
                :form="form"    
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
            >
            <div v-if="addCategoryOrFolder == 1">
                <a-form-item label="目录名称">
                    <a-input
                        v-decorator="[
                            'folder_name', 
                            { rules: [{ required: true, message: '请输入目录名称！' }] }
                        ]"
                        name="folder_name"
                        placeholder="请输入目录名称"
                    />
                </a-form-item>
            </div>
            <div v-else>
                <a-form-item label="目录名称">
                    <a-select
                        v-decorator="[
                        'parent_folder_id',
                        { rules: [{ required: true, message: '请选择目录!' }] },
                        ]"
                        placeholder="请选择目录"
                    >   
                        <a-select-option v-for="value, index in folder_list" v-bind:key="index" :value="value.folder_id">
                            {{value.folder_name}}
                        </a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item label="子目录">
                    <a-select
                        v-decorator="[
                            'child_folder_id'
                        ]"
                        placeholder="请选择子目录"
                    >  
                        <a-select-option v-for="value, index in child_folder_list" v-bind:key="index" :value="value.folder_id">
                            {{value.folder_name}}
                        </a-select-option>
                    </a-select>
                </a-form-item>
            </div>
            </a-form>
        </a-modal>
        <a-modal
            :visible="folderManageVisible"
            :confirm-loading="confirmLoading"
            @ok="handleFolderManageOK"
            @cancel="handleFolderManageCancel"
        >   
            <div style="margin-right: 20px">
                <div class='header-container'>
                    <span style="font-size:15px">标准目录管理</span>
                    <div>
                        <a-button v-if="!dragDisabled" @click="reorderSort" type="primary">重置排序</a-button>
                        <a-button v-if="!dragDisabled || folderEditEnable || folderDeleteEnable" @click="cancelFolderEdit" type="primary">取消</a-button>
                        <a-dropdown :trigger="['click']">
                            <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                                <a-button type="primary">操作</a-button>
                                <a-icon type="down"/>
                            </a>
                            <a-menu slot="overlay">
                                <a-menu-item key="1">
                                    <a @click="enableDrag" >排序</a>
                                </a-menu-item>
                                <a-menu-item key="2">
                                    <a @click="enableFolderEdit" >编辑</a>
                                </a-menu-item>
                                <a-menu-item key="3">
                                    <a @click="enableFolderDelete" >删除</a>
                                </a-menu-item>
                            </a-menu>    
                        </a-dropdown>  
                    </div>
                </div>
            </div>
            <hr>
            <a-form
                :form="form"    
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
            >
                <div class="treeDrag" style="margin-top: 1px; margin-bottom:1px">
                    <draggable 
                        :list="folderList" 
                        :group="{name: 'people'}"                         
                        @update="datadragEnd"
                        :disabled="dragDisabled"
                        v-bind="dragOptions"
                        @start="drag = true"
                        @end="drag = false"
                        ghost-class="ghostClass">
                        <div class="firstLevel" v-for="item in folderList" :key="item.folder_id" >
                            <div style="display:flex;justify-content: space-between; ">
                                <div class="leverFirst">
                                    <span>
                                        {{item.folder_name}}
                                    </span>
                                </div>
                                <a-button v-if="folderEditEnable" @click="handleEnableFolderNameEdit(item.folder_id)">编辑</a-button>
                                <a-button v-if="folderDeleteEnable" @click="handleFolderDelete(item.folder_id)">删除</a-button>
                            </div>
                            
                            <draggable 
                                :list="item.children" 
                                :options="{ forceFallback: true }"  
                                :sort="false" 
                                :group="{name: 'child'}" 
                                ghost-class="ghostClass" 
                                :disabled="dragDisabled"
                                >
                                <div class="SecondLevel" v-for="it in item.children" :key="it.folder_id">
                                    <div style="display:flex;justify-content: space-between; ">
                                        <div class="leverSecond">
                                            <span>
                                                {{it.folder_name}}
                                            </span>
                                        </div>
                                        <a-button v-if="folderEditEnable" @click="handleEnableFolderNameEdit(it.folder_id)">编辑</a-button>
                                        <a-button v-if="folderDeleteEnable" @click="handleFolderDelete(it.folder_id)">删除</a-button>
                                    </div>
                                </div>
                            </draggable>
                        </div>
                    </draggable>
                </div>
            </a-form>
        </a-modal>
        <a-modal
            :visible="editFolderNameVisible"
            :confirm-loading="confirmLoading"
            @ok="handleEditNameOk"
            @cancel="handleEditNameCancel"
        >   
            <span>编辑目录名称</span>
            <hr>
            <a-form
                :form="form"    
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
            >   
                <a-form-item label="原目录名称">
                <a-input
                    name="folder_name"
                    :defaultValue="needEditFolderOldName"
                    :disabled=true
                />
                </a-form-item>
                <a-form-item label="目录新名称">
                    <a-input
                        v-decorator="[
                        'folder_name', 
                        { rules: [{ required: true, message: '请输入目录名称！' }] }
                        ]"
                        name="folder_name"
                        placeholder="请输入目录名称"
                    />
                </a-form-item>
            </a-form>
        </a-modal>
        <a-modal
            :visible="uploadVisible"
            :confirm-loading="confirmLoading"
            @ok="handleUploadStandardOk"
            @cancel="handleUploadStandardCancel"
        >   
            <span>录入标准</span>
            <hr>
            <a-form
                :form="form"    
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
            >
            <a-form-item label="目录名称">
                <a-select 
                    v-decorator="[
                        'folder_id',
                        { rules: [{ required: true, message: '请选择目录!' }] },
                        ]"
                    placeholder="请选择目录"  
                    @change="handleAddFileFolderChange"
                    >
                        <a-select-option v-for="folder in folder_list" :key="folder.folder_id" >
                            {{ folder.folder_name }}
                        </a-select-option>
                </a-select>
            </a-form-item>
            <a-form-item label="子目录名称">
                <a-select 
                    v-decorator="[
                        'child_folder_id',
                        ]"
                    placeholder="子目录"  
                    >
                    <a-select-option 
                        v-for="value, index in add_file_child_folder_list" 
                        v-bind:key="index" 
                        :value="value.folder_id" 
                        >
                            {{value.folder_name}}
                    </a-select-option>
                </a-select>
            </a-form-item>
            <a-form-item label="标准名称">
                <a-input
                    v-decorator="[
                        'name', 
                        { rules: [{ required: true, message: '请输入标准名称！' }] }
                    ]"
                    placeholder="请输入标准名称"
                />
            </a-form-item>
            <a-form-item label="标准代号">
                <a-input
                    v-decorator="[
                        'standard_id', 
                        { rules: [{ required: true, message: '请输入标准代号！' }] }
                    ]"
                    placeholder="请输入标准代号"
                />
            </a-form-item>
            <a-form-item label="版本号">
                <a-input
                    placeholder="请输入版本号"
                    v-decorator="[
                        'version',
                        { rules: [{ required: true, message: '请输入版本号' }] }
                    ]"
                />
            </a-form-item>
            <a-form-item label="文件">
                <a-upload
                    :multiple="true"
                    :action="url.upload"
                    :file-list="fileList"
                    :headers="headers"
                    :disabled="disableUpload"
                    :before-upload="beforeUploadFile"
                    :data="{'type': uploadType, 'file_name': uploadedFileName}"
                    :showUploadList="true"
                    v-decorator="[
                        'file_path',
                        { rules: [{ required: true, message: '请上传文件!' }] },
                    ]"
                    @change="handleUploadFile"
                >
                    <a-button> <a-icon type="upload" /> 点击上传 </a-button>
                </a-upload>
            </a-form-item>
            </a-form>
        </a-modal>
        <hr style="margin-bottom:15px">
        <div>
            <div class="folder-selection">
                <span >标准目录 </span>
                <a-select :value="current_folder_id" placeholder="目录" style="width: 30%;font-size:18px; margin-left:10px;margin-right:10px" @change="handleFolderChange">
                    <a-select-option v-for="folder in folder_list" :key="folder.folder_id">
                        {{ folder.folder_name }}
                    </a-select-option>
                </a-select>
                <a-select :value="current_child_folder_id" placeholder="子目录" style="width: 30%;font-size:18px; margin-left:10px;margin-right:10px" @change="handleChildFolderChange">
                    <a-select-option v-for="child_folder in child_folder_list" :key="child_folder.folder_id">
                        {{ child_folder.folder_name }}
                    </a-select-option>
                </a-select>
            </div>              
            <div class="folder-selection">
                <span>查询条件 </span>
                <a-input-search 
                    style="width: 30%;font-size:18px; margin-left:10px;margin-right:10px"
                    placeholder="按标准号搜索" 
                    v-model="searchStandardId"
                    enter-button 
                    allowClear
                    @search="onSearch"/>
                <a-input-search 
                    style="width: 30%;font-size:18px; margin-left:10px;margin-right:10px"
                    placeholder="按标准名搜索" 
                    v-model="searchKeyword"
                    enter-button 
                    allowClear
                    @search="onSearch"/>
                <a-button type="primary" @click="handleReset">重置</a-button>
            </div>
            <a-table
                    :columns="columns"
                    :centered=true
                    :dataSource="file_list"
                    :rowKey='data=>file_list.index'
                    :pagination="pagination"
                    @change="handleTableChange"
                    class="data-table"
                >
                    <template slot="pdf_file" slot-scope="text, record">
                        <a-button @click="handleShowWordPreview(record)" type="primary"/>
                    </template>
                    <template slot="operation" slot-scope="text, record">
                        <a-dropdown :trigger="['click']">
                            <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                                <a-icon type="down"/>
                            </a>
                            <a-menu slot="overlay">
                                <a-menu-item key="1">
                                    <a  @click="handleGetStandard(record)">编辑</a>
                                </a-menu-item>
                                <a-menu-item key="2">
                                    <a @click="handleDeleteStandard(record)">删除</a>
                                </a-menu-item>
                                <a-menu-item key="3">
                                    <a :href="record.file_path" :download="record.file_name" target="_blank">下载</a>
                                </a-menu-item>
                            </a-menu>    
                        </a-dropdown>          
                    </template>
                </a-table>
                <a-modal
                    :visible="showDocPreview"
                    :confirm-loading="confirmLoading"
                    @ok="handleCloseWordPreview"
                    @cancel="handleCloseWordPreview"
                >   
                    <template>
                        <pdf 
                            :src="docUrl">
                        </pdf>
                    </template>
                </a-modal>
        </div>
    </div> 
</template>
<script>
import draggable from 'vuedraggable'
import { CreateFolder, QueryFolderList, StandardFileList, DeleteStandard, CreateStandard, FileDetail, FolerEdit, FolderDelete } from '@/api/StandardManagementApis'
import VueDocPreview from 'vue-doc-preview'
import Vue from 'vue';
import pdf from 'vue-pdf'

const columns2 = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
    width: '12%',
  },
  {
    title: 'Address',
    dataIndex: 'address',
    width: '30%',
    key: 'address',
  },
];


const columns = [
    {
    title: "序号",
    dataIndex: "index",
    align: "center",
    width: 100,
    scopedSlots: { customRender: "index" }
  },
  {
    title: "标准代号",
    dataIndex: "standard_id",
    align: "center",
    width: 300
  },
  {
    title: "标准名称",
    dataIndex: "standard_name",
    align: "center",
    width: 300
  },
  {
    title: "版本",
    dataIndex: "version",
    align: "center",
    width: 300
  },

  {
    title: "操作",
    dataIndex: "dataOperation",
    align: "center",
    width: 100,
    scopedSlots: { customRender: "operation" }
  }
];

const data2 = [{
        name: '我是一级分类1',
        id: 1,
        type:1,
        children: [{
          name: '我是二级分类10',
          id: 10,
          type:2
        }, {
          name: '我是二级分类11',
          id: 11,
          type:2
        }]
      }, {
        name: '我是一级分类2',
        id: 2,
        type:1,
        children: [{
          name: '我是二级分类20',
          id: 20,
          type:2
        }]
      },
      {
        name: '我是一级分类3',
        id: 3,
        type:1,
        children: [{
          name: '我是二级分类30',
          id: 31,
          type:2
        }]
      }
      ];

const rowSelection = {
  onChange: (selectedRowKeys, selectedRows) => {
    console.log(`selectedRowKeys: ${selectedRowKeys}`, 'selectedRows: ', selectedRows);
  },
  onSelect: (record, selected, selectedRows) => {
    console.log(record, selected, selectedRows);
  },
  onSelectAll: (selected, selectedRows, changeRows) => {
    console.log(selected, selectedRows, changeRows);
  },
};

export default {
    components: {
        draggable,
        pdf,
        VueDocPreview
    },
    data() {
        return {
            columns,
            categoryList: [],
            categoryFolderList: [],
            drag: false,
            addFolderVisible: false,
            folderManageVisible: false,
            uploadVisible: false,
            // form: this.$form.createForm(this),
            form: this.$form.createForm(this, { name: 'coordinated' }),
            labelCol: { span: 5 },
            wrapperCol: { span: 12 },
            confirmLoading: false,
            addCategoryOrFolder: 1, // true category; flase folder

            deleteDisabled: true,
            deletedFolder: [],
            deletedCategory: [],
            oldCategoryFolderList: [],
            pagination: {}, //分页,
            file_list: [],
            // 目录
            folder_list: [], 
            folder_map_child_dict: {},
            child_folder_list: [],
            current_folder_id: undefined,
            current_child_folder_id: undefined,
            // 搜索
            searchKeyword: "",
            searchStandardId: "",
            // 文件相关 - todo: 加上上传人
            uploadType: "standard", 
            headers: {
            },
            url: {
                upload: "http://localhost:9023/files/upload_files", //上传文件
            },
            uploadedFileName: "测试", // 进行删除
            add_file_child_folder_list: [],
            add_file_current_folder_id: undefined,
            uploaded_file_path: undefined,
            uploaded_file_uuid: undefined,
            disableUpload: false,
            fileList: [],
            
            // 修改目录
            dragDisabled: true,
            orgFolderList: [],
            folderEditEnable: false,
            folderDeleteEnable: false,
            editFolderNameVisible: false,
            needEditFolderId: undefined,
            needEditFolderOldName: "test",
            folderList: undefined,

            // 测试
            
            rowSelection,
            columns2,

            // 预览
            docUrl: undefined,
            showDocPreview: false,


        }
    },

    mounted() {
        this.queryFolders() // 查询文件夹列表
        this.queryStandardFiles() // 查询文件列表
    },

    methods: {
        handleTableChange(pagination, filters, sorter) {//表格点击事件
            const pager = { ...this.pagination };
            pager.current = pagination.current;
            this.pagination = pager;
            const param = {
                sort_field: sorter.field,
                sort_order: sorter.order,
                search_keyword: this.searchKeyword,
                search_standard_id: this.searchStandardId,
            }
            
            this.queryStandardFiles(param); //查询列表
        },
        
        // 目录列表
        queryFolders() {
            console.log("获取目录")
            QueryFolderList()
                .then(res => {
                    if(res.code == '1'){
                        this.folder_list = res.data;    
                        this.folderList = res.data;  
                        for (var i = 0; i < res.data.length; i++) {
                            this.folder_map_child_dict[res.data[i].folder_id] = res.data[i].children
                        }
                }})
                .catch(err => {});
        },

        
        // 标准列表
        // -- 查询条件
        handleFolderChange(value) {
            this.child_folder_list = this.folder_map_child_dict[value];
            this.current_folder_id = value
        },

        handleChildFolderChange(value) {
            this.current_child_folder_id = value
        },

        onSearch(value) {
            this.queryStandardFiles({
                sort_field: "",
                sort_order: "",
                search_keyword: this.searchKeyword,
                search_standard_id: this.searchStandardId,
                folder_id: this.current_folder_id,
                child_folder_id: this.current_child_folder_id,
            })
        },

        handleReset() {
            console.log("重置")
            this.searchStandardId = ""
            this.searchKeyword = ""
            this.current_folder_id = undefined
            this.current_child_folder_id = undefined
            this.child_folder_list = []
            this.queryStandardFiles()
        },

        queryStandardFiles(param) {
            StandardFileList(param)
                .then(res => {
                    if(res.code == '1'){
                        this.file_list = res.data.content;                        
                        const pagination = { ...this.pagination };
                        pagination.total = res.data.total_elements;
                        pagination.showTotal = () => `共${pagination.total}条数据`;
                        this.pagination = pagination;
                }})
                .catch(err => {});
        },

        // 文件操作：删除
        handleDeleteStandard(record) {
            const param = {
                file_id: record.file_id,
            }
            DeleteStandard(param)
                .then(res => {
                    if (res.code == '1') {
                        this.$message.info("文件删除成功", 2)
                        this.queryStandardFiles()
                    } else {
                        this.$message.error(res.msg, 2)
                    }}
                ).catch(err => {
                    this.$message.error(err.msg, 2)
            })
        },

        // 文件操作：上传文件相关function
        beforeUploadFile(file) {
            const isLt10M = file.size / 1024 / 1024 < 50;
            this.uploadedFileName = file.name
            if (!isLt10M) {
                this.$message.error('上传的图片需小于 50MB!');
            }
            
            return isLt10M;
        },
        
        // 上传文件
        handleUploadFile(info) {
            let { fileList } = info
            const status = info.file.status
            if (status === 'done') {
                this.$message.success('文件上传成功...', 1)
                this.disableUpload = true
                this.uploaded_file_path = info.file.response.data.file_path
                this.uploaded_file_uuid = info.file.response.data.uid
                                
            } else if (status === 'error') {
                this.$message.error(`${info.file.name} 文件上传失败`)
                this.disableUpload = false
            } else if (status === 'uploading') {
                console.log(info)
            }
            this.fileList= [...fileList]
        },

        handleAddFileFolderChange(value) {
            this.add_file_child_folder_list = this.folder_map_child_dict[value];
            this.add_file_current_folder_id = value
        },

        handleClick(folder_info) {
            if (this.dragDisabled) {
                Vue.ls.set("CurrentFolder", folder_info.folder_name)
                Vue.ls.set("CurrentFolderId", folder_info.folder_id)
                this.$router.push({ name: 'fileList'})
            }
            
        },
        // 显示新增文件夹
        showAddFolder() {
            this.addFolderVisible = true;
        },
        // 现实标准目录管理界面
        showFolderManage() {
            this.folderManageVisible = true;
            this.orgFolderList = JSON.parse(JSON.stringify(this.folderList));
        },

        // 实现编辑
        enableFolderEdit() {
            this.folderEditEnable = true;
            this.folderDeleteEnable = false;
            this.dragDisabled = true;
        },

        // 实现文件夹删除
        enableFolderDelete() {
            this.folderEditEnable = false;
            this.folderDeleteEnable = true;
            this.dragDisabled = true;
        },
        // 显示标准录入页面
        showUploadFile() {
            this.uploadVisible = true;
        },

        // 新增标准目录和标准子目录
        handleAddFolderOk(e) {
            //e.preventDefault();
            if (this.addCategoryOrFolder == 1) {
                this.form.validateFields((err, values) => {
                    CreateFolder(values)
                        .then(res => {
                            if(res.code == "1"){
                                this.$message.info("创建成功", 1)
                                this.queryFolders()
                                this.addFolderVisible = false

                            } else {
                                this.$message.warning(res.msg, 1)
                            }
                        })
                }).catch( err => {})
            } else {
                this.form.validateFields((err, values) => {
                    CreateFolder(values)
                        .then(res => {
                            if(res.code == "1"){
                                this.$message.info("创建成功", 1)
                                this.queryFolders()
                                this.addFolderVisible = false
                            } else {
                                this.$message.warning(res.msg, 1)
                            }
                        })
                }).catch( err => {})
            }
            
            //this.addFolderVisible = false;
            // this.addFileForm.resetFields();
        },

        clearFile() {
    	    this.fileList = []
        },
        
        // 取消新增标准目录
        handleAddFolderCancel(e) {
            this.addFolderVisible = false;
            // this.addFileForm.resetFields()
        },

        // 标准目录管理
        handleFolderManageCancel(e) {
            this.folderManageVisible = false;
            this.cancelFolderEdit()
            // this.addFileForm.resetFields()
        },

        // 标准目录管理确认
        handleFolderManageOK(e) {
            this.folderManageVisible = false;
            // this.addFileForm.resetFields()
        },
        
        // 取消录入标准
        handleUploadStandardCancel(e) {
            this.uploadVisible = false;
            this.form.resetFields()
            this.disableUpload = false
            this.uploaded_file_path = undefined
            this.uploaded_file_uuid = undefined
            this.clearFile()
        },
        // 录入标准
        handleUploadStandardOk() {
            this.form.validateFields((err, values) => {
                    const param = {...values}
                    param.file_path = this.uploaded_file_path
                    param.file_uid = this.uploaded_file_uuid
                    CreateStandard(param).then(res => {
                            const respCode = res.code
                            if (respCode == 1) {
                                this.$message.info("标准创建成功", 1)
                                this.uploadVisible = false;
                                this.form.resetFields()
                                this.disableUpload = false
                                this.uploaded_file_path = undefined
                                this.uploaded_file_uuid = undefined
                                this.queryStandardFiles() // 查询文件列表
                            } else {
                                this.$message.error(res.msg, 1)
                            }
                            
                        })

                }).catch( err => {})
        },

        // 编辑标准信息
        handleGetStandard(record) {
            this.uploadVisible = true,
            this.editDisabled = true
            this.saveOrEdit = true
            this.form.resetFields();
            const param = {
                "file_id": record.file_id
            }
            FileDetail(param)
                .then(response => {
                    this.record = {
                        standard_id: response.data.standard_id,
                        name: response.data.name,
                        file_path: response.data.file_path,
                        folder_id: response.data.folder_id,
                        child_folder_id: response.data.child_folder_id,
                        version: response.data.version,
                    }
                    const file = {
                        file_id: response.data.file_id,
                        name: response.data.name,
                        url: response.data.file_path,
                        status: "done",
                    }
                    this.fileList = [
                        {
                        uid: '-1',
                        name: response.data.name,
                        status: 'done',
                        url: response.data.file_path,
                        },
                    ],
                    console.log(this.fileList)
                    this.$nextTick(() => {  
                        this.form.setFieldsValue(this.record);
                    })  
                })
                .catch(error => {
                    this.$message.error(error.msg, 1)

                })
            
    
        },

        // 显示新增文件夹
        enableDrag() {
            this.dragDisabled = false;
            this.folderEditEnable = false;
            this.folderCancelEnable = false;
        },

        // 重置排序
        reorderSort() {
            this.folderList = JSON.parse(JSON.stringify(this.orgFolderList));
        },

        // 重置排序
        cancelFolderEdit() {
            this.folderList = JSON.parse(JSON.stringify(this.orgFolderList));
            this.dragDisabled = true;
            this.folderEditEnable = false;
            this.folderDeleteEnable = false;
        },


        onChange(e) {
            this.addCategoryOrFolder = e.target.value;
        },
        getdata (evt) {
            console.log(evt.draggedContext.element.id)
        },
        datadragEnd (evt) {
            
        },
        
        // 目录编辑
        handleEnableFolderNameEdit(folder_id){
            this.editFolderNameVisible = true;
            this.needEditFolderId = folder_id
        },

        handleFolderDelete(folder_id){
            const that = this
            const param = {
                "folder_id": folder_id,
            }
            this.$confirm({
                title: "提示",
                centered: true,
                okText: "确定",
                cancelText: "取消",
                content: '确认删除？',
                onOk() {
                    FolderDelete(param)
                        .then(resp => {
                            if (resp.code == 1) {
                                that.$message.info("删除成功", 1)
                                that.form.resetFields()
                                that.queryFolders() // 查询文件列表
                                
                            } else {
                                that.$message.error(res.msg, 1)
                                that.form.resetFields()
                            }
                        })
                        .catch(err => {})
                    
                },
                onCancel() {
            }
            });
        },

        handleEditNameOk(){
            this.form.validateFields((err, values) => {
                    const param = {...values}
                    param.folder_id = this.needEditFolderId
                    console.log("编辑ok")
                    console.log(param)
                    FolerEdit(param).then(res => {
                            const respCode = res.code
                            if (respCode == 1) {
                                this.$message.info("编辑成功", 1)
                                this.form.resetFields()
                                this.editFolderNameVisible = false;
                                this.needEditFolderId = undefined
                                this.queryFolders() // 查询文件列表
                            } else {
                                this.$message.error(res.msg, 1)
                                this.form.resetFields()
                            }
                            
                        })

                }).catch( err => {})
            this.editFolderNameVisible = false;

        },

        handleEditNameCancel(){
            this.editFolderNameVisible = false;
            this.edit
        },

        handleShowWordPreview(record) {
            this.docUrl = record.file_path
            this.showDocPreview = true
        },

        handleCloseWordPreview() {
            this.docUrl = undefined
            this.showDocPreview = false
        }


        

    },
    computed: {
        dragOptions() {
        return {
            animation: 0,
            group: "description",
            disabled: false,
            ghostClass: "ghost"
        };
        }
    }
};
</script>
<style>
.header-container{
line-height: 40px; 
   display: flex;
   justify-content: space-between;

}
.folder-list {
    display: flex;
    flex-wrap: wrap;
    margin: 12px 12px;
}

.folder-selection {
    font-size: 20px;
    font-style: bold;
    display: flex;
    flex-wrap: wrap;
    margin: 12px 12px;
    height: 40px;
}

.folder-label-wrapper {
    display: flex;
    flex-direction: row;
    align-items: baseline;
    
}
.folder-container {
    position: relative;
    vertical-align: bottom;
    display: inline-block;
    text-align: center;
    margin: 0 12px;
    width: 120px;
}

.search-box {
    margin: 12px 12px;
    width: 30%;
}

.delete {
    position: absolute;
    top: 0px;
    right: 0px;
}

.caption {
    display: block;
}
.button {
  margin-top: 35px;
}
.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
}
.list-group {
  min-height: 20px;
}
.list-group-item {
  cursor: move;
}
.list-group-item i {
  cursor: pointer;
}
.leverFirst {
    display: flex;
    justify-content: space-between;
    border: 1px solid;
    width: 50%;
    line-height: 40px;
    margin-top: 1px;
    margin-bottom: 1px;
}
.leverSecond {
    display: flex;
    justify-content: space-between;
    border: 1px solid;
    width: 50%;
    line-height: 40px;
    margin-left: 30px;
    margin-top: 1px;
    margin-bottom: 1px;
    
}
</style>
