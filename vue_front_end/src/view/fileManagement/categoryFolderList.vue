<template>
    <div class="folder-wrapper">
        <div class="header-container">
            <h1 style="font-size:30px">文件管理</h1>
            <div :trigger="['click']">
                        <a-button v-if="!dragDisabled" type="primary" @click="sort">重置</a-button>
                        <a-button v-if="!dragDisabled" type="primary" @click="handleSubmit">提交</a-button>
                        <a-button v-if="!dragDisabled" type="primary" @click="handleCancle">取消</a-button>
                        <a-dropdown>
                            <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                                <a-button type="primary">操作</a-button> <a-icon type="down"/>
                            </a>
                            <a-menu slot="overlay">
                                <a-menu-item key="1">
                                    <a @click="showAddFolder">新增分类/文件夹</a>
                                </a-menu-item>
                                <a-menu-item key="2">
                                    <a @click="handleEnableDrag">排序与删除</a>
                                </a-menu-item>
                            </a-menu>    
                        </a-dropdown>
            </div>
        </div>
        <hr style="margin-bottom:15px">
        <div>
            <div v-for="category, cat_index in categoryFolderList" class="category-list" :key="cat_index">
                <div :style="{'display': 'flex', 'justify-content': cat_index === 0? 'space-between':'flex-start'}">
                    <div class="category-name">
                        <label style="font-size:25px;font-style:bold"> {{category.category_name}}</label>
                        <button v-if="!deleteDisabled" @click="handleDeleteCategory(category.category_id, cat_index)">X</button>
                    </div>
                    
                </div>
                <div class="folder-list">
                    <draggable 
                        v-model="category.data" 
                        :move="getdata" 
                        @update="datadragEnd"
                        v-bind="dragOptions"
                        :disabled="dragDisabled"
                        @start="drag = true"
                        @end="drag = false"
                        >
                        <transition-group>
                            <div 
                                class="folder-container"
                                v-for="folder_info, folder_index in category.data"  
                                :key="folder_index">
                                <button v-if="!deleteDisabled" @click="handleDeleteFolder(folder_info.folder_id, folder_index, category.category_index)" class="delete">X</button>
                                <img src="../../../static/folder.svg" style="width:100px;height:100px" @click="handleClick(folder_info)"/>
                                <span class="caption">{{folder_info.folder_name}}</span>
                            </div>
                        </transition-group>
                    </draggable>
                </div>
            </div>
        </div>
        <a-modal
            :visible="addFolderVisible"
            :confirm-loading="confirmLoading"
            @ok="handleAddFolderOk"
            @cancel="handleAddFolderCancel"
        >   
            <div>
                <a-radio-group v-model="addCategoryOrFolder" default-value=1 button-style="solid" @change="onChange">
                    <a-radio-button value=1>
                        新增分类
                    </a-radio-button>
                    <a-radio-button value=2>
                        新增文件夹
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
                <a-form-item label="分类名称">
                    <a-input
                        v-decorator="[
                            'category_name', 
                            { rules: [{ required: true, message: '请输入分类名称！' }] }
                        ]"
                        name="categoryName"
                        placeholder="请输入分类名称"
                    />
                </a-form-item>
            </div>
            <div v-else>
                <a-form-item label="分类名称">
                    <a-select
                        v-decorator="[
                        'category_id',
                        { rules: [{ required: true, message: '请选择分类!' }] },
                        ]"
                        placeholder="请选择分类"
                    >   
                        <a-select-option v-for="value, index in categoryList" v-bind:key="index" :value="value.category_id">
                            {{value.category_name}}
                        </a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item label="文件夹名称">
                    <a-input
                        v-decorator="[
                            'folder_name', 
                            { rules: [{ required: true, message: '请输入文件夹名称！' }] }
                        ]"
                        placeholder="请输入文件夹名称"
                    />
                </a-form-item>
            </div>
            </a-form>
        </a-modal>
    </div> 
</template>
<script>
import draggable from 'vuedraggable'
import { getCategorFolderList, getCategoryList, createCategory, createFolder, updateCategoryAndFolder } from '@/api/filesManager'
import Vue from 'vue';
export default {
    components: {
        draggable
    },
    data() {
        return {
            categoryList: [],
            categoryFolderList: [],
            drag: false,
            addFolderVisible: false,
            // form: this.$form.createForm(this),
            form: this.$form.createForm(this, { name: 'coordinated' }),
            labelCol: { span: 5 },
            wrapperCol: { span: 12 },
            confirmLoading: false,
            addCategoryOrFolder: 1, // true category; flase folder
            dragDisabled: true,
            deleteDisabled: true,
            deletedFolder: [],
            deletedCategory: [],
            oldCategoryFolderList: [],
            pagination: {}, //分页
        }
    },

    mounted() {
        this.queryFolders() // 查询文件夹列表
        this.queryCategorys() // 查询文件分类列表
    },

    methods: {
        // 文件列表
        queryFolders() {
            getCategorFolderList()
                .then(res => {
                    if(res.code == '1'){
                        this.categoryFolderList = res.data;
                        for (var i = 0; i < this.categoryFolderList.length; i++) {
                            this.categoryFolderList[i].data.sort(function(a, b) { return a.sort_order - b.sort_order; });
                        }
                }})
                .catch(err => {});
        },
        queryCategorys() {
            getCategoryList()
                .then(res => {
                    if(res.code == '1'){
                        this.categoryList = res.data;
                }})
                .catch(err => {});
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
        handleAddFolderOk(e) {
            //e.preventDefault();
            if (this.addCategoryOrFolder == 1) {
                this.form.validateFields((err, values) => {
                    createCategory(values)
                        .then(res => {
                            if(res.code == "1"){
                                this.$message.info("创建成功", 1)
                                this.queryCategorys()
                                this.queryFolders()
                                this.addFolderVisible = false

                            } else {
                                this.$message.warning(res.msg, 1)
                            }
                        })
                }).catch( err => {})
            } else {
                this.form.validateFields((err, values) => {
                    createFolder(values)
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
        
        handleAddFolderCancel(e) {
            this.addFolderVisible = false;
            // this.addFileForm.resetFields()
        },
        handleAddFolder() {
            console.log("add folder")
        },
        onChange(e) {
            this.addCategoryOrFolder = e.target.value;
        },
        getdata (evt) {
            console.log(evt.draggedContext.element.id)
        },
        datadragEnd (evt) {
            
        },
        sort() {
            // for (var i = 0; i < this.categoryList.length; i++) {
            //     this.categoryList[i].data.sort(function(a, b) { return a.sort_order - b.sort_order; });
            // }
            this.deletedFolder = []
            this.categoryFolderList = JSON.parse(JSON.stringify(this.OldCategoryFolderList))
        },
        handleEnableDrag() {
            this.dragDisabled = false
            this.deleteDisabled = false
            this.OldCategoryFolderList = JSON.parse(JSON.stringify(this.categoryFolderList))
        },
        handleCancle() {
            this.dragDisabled = true
            this.deleteDisabled = true
            this.deletedFolder = []
            this.categoryFolderList = JSON.parse(JSON.stringify(this.OldCategoryFolderList))
            this.OldCategoryFolderList = []
        },
        handleDeleteFolder(folder_id, folder_index, category_index) {
            this.deletedFolder.push(folder_id)
            this.categoryFolderList[category_index].data.splice(folder_index, 1);
        },
        handleDeleteCategory(category_id, category_index) {
            this.deletedCategory.push(category_id)
            this.categoryFolderList.splice(category_index, 1);
        },
        handleSubmit() {
            const tmpFolderCategoryList = []
            for (var i = 0; i < this.categoryFolderList.length; i++) {
                const tmpFolderList = []
                const tmpFoldersInfo = this.categoryFolderList[i].data
                for (var k = 0; k < tmpFoldersInfo.length; k++) {
                    tmpFolderList.push(tmpFoldersInfo[k].folder_id)
                }
                const tmpFolderListStr = tmpFolderList.join()
                const tmpFolderCategory = this.categoryFolderList[i].category_id + "_" + tmpFolderListStr
                tmpFolderCategoryList.push(tmpFolderCategory)
            }
            const param = {
                deleted_categories: this.deletedCategory.join(),
                delete_folders: this.deletedFolder.join(),
                folder_categories: tmpFolderCategoryList.join("|")
            }
            updateCategoryAndFolder(param)      
                .then(response => {
                    if (response.code == 1) {
                        this.$message.info("提交成功", 1)
                        this.queryCategorys()
                        this.queryFolders()
                        this.dragDisabled = true
                        this.deleteDisabled = true
                        this.OldCategoryFolderList = []
                    } else {
                        this.$message.warning(response.msg, 1)
                    }
                })
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
</style>
