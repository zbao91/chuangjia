<template>
    <div class="folder-wrapper">
        <div class="header-container">
            <h1 style="font-size:30px">图号管理</h1>
        </div>
        <hr style="margin-bottom:15px">
        <div class="header-container">
            <a-radio-group default-value="a" button-style="solid">
                <a-radio-button @click="imageQuery" value="a">
                    图号查询
                </a-radio-button>
                <a-radio-button @click="imageManage" value="b">
                    图号台帐
                </a-radio-button>
                <a-radio-button @click="imageApplicationPage" value="d">
                    图号申请
                </a-radio-button>
                <a-radio-button @click="imageRuleCreate" value="c">
                    图号规则
                </a-radio-button>
            </a-radio-group>
            <div>
                <a-button @click="enableImageRuleAdd" type="primary">规则新增</a-button>
                <a-button @click="enableImageApplication" type="primary">图号申请</a-button>
            </div>
            <a-modal
                :visible="imageApplication"
                :confirm-loading="confirmLoading"
                @ok="handleImageApplicationOk"
                @cancel="handleImageApplicationCancel"
            >   
            <span>图号申请</span>
            <hr>
            <a-form
                :form="applicationForm"    
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
            >
            <div>
                <a-form-item label="客户">
                    <a-input
                        v-decorator="[
                            'customer_name',
                            { rules: [{ required: true, message: '请输入客户！' }] },
                        ]"
                        placeholder="请输入客户"
                    />
                </a-form-item>
                <a-form-item label="车型">
                    <a-input
                        v-decorator="[
                            'vehicle_model',
                            { rules: [{ required: true, message: '请输入车型！' }] },
                        ]"
                        placeholder="请输入车型"
                        :disabled="imageEdit"
                    />
                </a-form-item>
                <a-form-item label="产品名">
                    <a-input
                        v-decorator="[
                            'product_name',
                            { rules: [{ required: true, message: '请输入产品名！' }] },
                        ]"
                        placeholder="请输入产品名"
                    />
                </a-form-item>
                <a-form-item label="产品品类">
                    <a-select
                        v-decorator="[
                            'product_info',
                            { rules: [{ required: true, message: '请输入并选择产品品类！' }] },
                        ]"
                        show-search
                        label-in-value
                        placeholder="请输入并选择产品品类"
                        :default-active-first-option="false"
                        :show-arrow="true"
                        :filter-option="false"
                        :disabled="imageEdit"
                        @search="onSearchProductName"
                        @change="onChange"
                        @select="onSelectProductName"
                    >
                        <a-select-option v-for="d in dataSource" :key="d.id" :data="d.has_dimension">
                            {{ d.show_name }}
                        </a-select-option>
                    </a-select>
                </a-form-item>
                <a-form-item v-if="hasDimensionApply" label="直径">
                    <a-input
                        v-decorator="[
                            'product_diameter',
                            { rules: [{ required: true, message: '请输入产品直径！' }] },
                        ]"
                        placeholder="请输入产品直径"
                        :disabled="imageEdit"
                    />
                </a-form-item>
                <a-form-item v-if="hasDimensionApply" label="长度">
                    <a-input
                        v-decorator="[
                            'product_length',
                            { rules: [{ required: true, message: '请输入产品长度！' }] },
                        ]"
                        placeholder="请输入产品长度"
                        :disabled="imageEdit"
                    />
                </a-form-item>
                <a-form-item label="客户品号">
                    <a-input
                        v-decorator="[
                            'product_cid',
                        ]"
                        placeholder="请输入客户品号"
                    />
                </a-form-item>
                <a-form-item label="配套描述">
                    <a-textarea
                        v-decorator="[
                            'product_description',
                        ]"
                        placeholder="请输入配套描述"
                    />
                </a-form-item>
            </div>
            </a-form>
        </a-modal>
        </div>
        <div v-if="pageType == 1" class="image-query">            
            <div class="folder-selection">
                <a-dropdown :trigger="['click']">
                    <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                        <a-button type="primary">查询条件</a-button>
                        <a-icon type="down"/>
                    </a>
                    <a-menu slot="overlay">
                        <a-menu-item key="1">
                            <a @click="searchByImageId">按图号</a>
                        </a-menu-item>
                        <a-menu-item key="2">
                            <a @click="searchByProductName">按产品名称</a>
                        </a-menu-item>
                        <a-menu-item key="3">
                            <a @click="searchByCustomerName" >按客户名称</a>
                        </a-menu-item>
                        <a-menu-item key="4">
                            <a @click="searchByVehicleModel" >按车型名称</a>
                        </a-menu-item>
                        <a-menu-item key="5">
                            <a @click="searchByApplicant" >按申请人</a>
                        </a-menu-item>
                    </a-menu>    
                </a-dropdown>  
                <a-input-search 
                    style="width: 30%;font-size:18px; margin-left:10px;margin-right:10px"
                    :placeholder="searchBarPlaceholder" 
                    v-model="searchKeyword"
                    enter-button 
                    allowClear
                    @search="onSearchTab1"/>
                <a-button @click="resetImageQuery" style="primary">重置</a-button>
            </div>
            <div v-if="hasQueried" class="query-result">
                <a-table
                    :columns="columnsImageQuery"
                    :centered=true
                    :dataSource="searchResultTab1"
                    :rowKey='searchResultTab1=>searchResultTab1.index'
                    :pagination="pagination"
                    @change="handleTableChange"
                    class="data-table"
                >
                </a-table>
            </div>
            <div v-else>
                <img style="width:100%" src="../../../static/image_rules.png"/>
            </div>
        </div>
        <div v-else-if="pageType == 2" class="images-list">
            <div class="folder-selection">
                <a-dropdown :trigger="['click']">
                    <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                        <a-button type="primary">查询条件</a-button>
                        <a-icon type="down"/>
                    </a>
                    <a-menu slot="overlay">
                        <a-menu-item key="1">
                            <a @click="searchByProductName">按产品名称</a>
                        </a-menu-item>
                        <a-menu-item key="2">
                            <a @click="searchByCustomerName" >按客户名称</a>
                        </a-menu-item>
                        <a-menu-item key="3">
                            <a @click="searchByVehicleModel" >按车型名称</a>
                        </a-menu-item>
                    </a-menu>    
                </a-dropdown>  
                <a-input-search 
                    style="width: 30%;font-size:18px; margin-left:10px;margin-right:10px"
                    :placeholder="searchBarPlaceholder" 
                    v-model="searchKeyword"
                    enter-button 
                    allowClear
                    @search="onSearchTab2"/>
                <a-button @click="resetImageQuery" style="primary">重置</a-button>
            </div>
            <div>
                <a-table
                    :columns="columnsImageManage"
                    :centered=true
                    :dataSource="searchResultTab2"
                    :rowKey='searchResultTab2=>searchResultTab2.index'
                    :pagination="pagination"
                    @change="handleTableChange"
                    class="data-table"
                >
                    <template v-if="pageType == 2" slot="operation" slot-scope="text, record">
                        <a-dropdown :trigger="['click']">
                            <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                                <a-icon type="down"/>
                            </a>
                            <a-menu slot="overlay">
                                <a-menu-item key="1">
                                    <a  @click="handleImageEdit(record)">编辑</a>
                                </a-menu-item>
                                <a-menu-item key="2">
                                    <a @click="handleDeleteImage(record)">删除</a>
                                </a-menu-item>
                            </a-menu>    
                        </a-dropdown>          
                    </template>
                </a-table>
            </div>
        </div>
        <div v-else-if="pageType == 4" class="images-application">
            <div class="folder-selection">
                <a-dropdown :trigger="['click']">
                    <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                        <a-button type="primary">查询条件</a-button>
                        <a-icon type="down"/>
                    </a>
                    <a-menu slot="overlay">
                        <a-menu-item key="1">
                            <a @click="searchByProductName">按产品名称</a>
                        </a-menu-item>
                        <a-menu-item key="2">
                            <a @click="searchByCustomerName" >按客户名称</a>
                        </a-menu-item>
                        <a-menu-item key="3">
                            <a @click="searchByVehicleModel" >按车型名称</a>
                        </a-menu-item>
                        <a-menu-item key="4">
                            <a @click="searchByApplicant" >按申请人</a>
                        </a-menu-item>
                    </a-menu>    
                </a-dropdown>  
                <a-input-search 
                    style="width: 30%;font-size:18px; margin-left:10px;margin-right:10px"
                    :placeholder="searchBarPlaceholder" 
                    v-model="searchKeyword"
                    enter-button 
                    allowClear
                    @search="onSearchTab2"/>
                <a-button @click="resetImageQuery" style="primary">重置</a-button>
            </div>
            <div>
                <a-table
                    :columns="columnsImageApplication"
                    :centered=true
                    :dataSource="searchResultTab4"
                    :rowKey='searchResultTab4=>searchResultTab4.index'
                    :pagination="pagination"
                    @change="handleTableChange"
                    class="data-table"
                >
                    <template v-if="pageType == 4" slot="approve" slot-scope="text, record">
                        <a-button type="primary" @click="handleApplicationPass(record)">通过</a-button>
                        <a-button type="danger" @click="handleApplicationDeny(record)">不通过</a-button>         
                    </template>
                </a-table>
            </div>
        </div>
        <div v-else-if="pageType == 3" class="images-rule">
            <div class="folder-selection">
                <a-dropdown :trigger="['click']">
                    <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                        <a-button type="primary">查询条件</a-button>
                        <a-icon type="down"/>
                    </a>
                    <a-menu slot="overlay">
                        <a-menu-item key="1">
                            <a @click="searchByProductNameEnAndCHN">按产品名称（中英文）</a>
                        </a-menu-item>
                        <a-menu-item key="2">
                            <a @click="searchByProductType">按产品类型</a>
                        </a-menu-item>
                    </a-menu>    
                </a-dropdown>  
                <a-input-search 
                    style="width: 30%;font-size:18px; margin-left:10px;margin-right:10px"
                    :placeholder="searchBarPlaceholder" 
                    v-model="searchKeyword"
                    enter-button 
                    allowClear
                    @search="onSearchTab2"/>
                <a-button @click="resetImageQuery" style="primary">重置</a-button>
            </div>
            <div>
                <a-table
                    :columns="columnsRules"
                    :centered=true
                    :dataSource="searchResultTab3"
                    :rowKey='searchResultTab3=>searchResultTab3.index'
                    :pagination="pagination"
                    @change="handleTableChange"
                    class="data-table"
                >
                    <template v-if="pageType == 3" slot="operation" slot-scope="text, record">
                        <a-dropdown :trigger="['click']">
                            <a class="ant-dropdown-link" @click="e => e.preventDefault()">
                                <a-icon type="down"/>
                            </a>
                            <a-menu slot="overlay">
                                <a-menu-item key="1">
                                    <a @click="handleRuleEdit(record)">编辑</a>
                                </a-menu-item>
                                <a-menu-item key="2">
                                    <a @click="handleDeleteRule(record)">删除</a>
                                </a-menu-item>
                            </a-menu>    
                        </a-dropdown>          
                    </template>
                </a-table>
            </div>
        </div>
        <a-modal
                :visible="imageRuleAdd"
                :confirm-loading="confirmLoading"
                @ok="handleImageAddRuleOk"
                @cancel="handleImageAddRuleCancel"
            >   
            <span v-if="ruleEdit">图号规则修改</span>
            <span v-else>图号规则添加</span>
            <hr>
            <a-form
                :form="ruleForm"    
                :label-col="labelCol"
                :wrapper-col="wrapperCol"
                
            >
            <div>
                <a-form-item v-if="ruleEdit" label="原产品中文名称">
                    <a-input
                        style="margin-left: 10px"
                        v-decorator="[
                            'old_product_name_chn',
                        ]"
                        :disabled="ruleEdit"
                    />
                </a-form-item>
                <a-form-item v-if="ruleEdit" label="请输入产品分类代号！">
                    <a-input
                        style="margin-left: 10px"
                        v-decorator="[
                            'old_product_cid',
                        ]"
                        :disabled="ruleEdit"
                    />
                </a-form-item>
                <a-form-item label="产品分类代号">
                    <a-input
                        style="margin-left: 10px"
                        v-decorator="[
                            'product_cid',
                            { rules: [{ required: true, message: '请输入产品分类代号！' }] },
                        ]"
                        placeholder="请输入产品分类代号"
                    />
                </a-form-item>
                <a-form-item label="产品类型">
                    <a-input
                        style="margin-left: 10px"
                        v-decorator="[
                            'product_type',
                            { rules: [{ required: true, message: '请输入产品类型！' }] },
                        ]"
                        placeholder="请输入产品类型"
                    />
                </a-form-item>
                <a-form-item label="产品中文名称">
                    <a-input
                        style="margin-left: 10px"
                        v-decorator="[
                            'product_name_chn',
                            { rules: [{ required: true, message: '请输入产品中文名称！' }] },
                        ]"
                        placeholder="请输入产品中文名称"
                    />
                </a-form-item>
                <a-form-item label="产品英文名称">
                    <a-input
                        style="margin-left: 10px"
                        v-decorator="[
                            'product_name_en',
                        ]"
                        placeholder="请输入产品英文名称"
                    />
                </a-form-item>
                <a-form-item label="产品备注">
                    <a-textarea
                        style="margin-left: 10px"
                        v-decorator="[
                            'product_remarks',
                        ]"
                        placeholder="请输入产品备注"
                    />
                </a-form-item>
                <a-form-item label="需要输入尺寸">
                    <a-switch 
                        style="margin-left: 10px"
                        v-decorator="[
                            'has_dimension',
                        ]"
                        checked-children="是" 
                        un-checked-children="否" 
                        :checked="ruleDetailHasDimension" />
                </a-form-item>
                <a-form-item label="需要顺延后四位">
                    <a-switch 
                        style="margin-left: 10px"
                        v-decorator="[
                            'has_auto_increase',
                        ]"
                        checked-children="是" 
                        un-checked-children="否" 
                        :checked="ruleDetailHasSpec" />
                </a-form-item>            
            </div>
            </a-form>
        </a-modal>
    </div> 
</template>
<script>
import draggable from 'vuedraggable'
import { ImageApply, ImageApplications, ImageApplicationPass, ImageApplicationDeny, ImageList, AddImageRule, 
        ImageRuleList, DeleteImageRule, SearchRule, ImageDetail, ImageDelete, RuleDetail } from '@/api/ImageManagementApis.js'
import Vue from 'vue';
import pdf from 'vue-pdf'

const role = "admin"

const columnsImage = [
    {
    title: "序号",
    dataIndex: "index",
    align: "center",
    width: 100,
    scopedSlots: { customRender: "index" }
  },
  {
    title: "客户",
    dataIndex: "customer_name",
    align: "center",
    width: 300
  },
  {
    title: "车型",
    dataIndex: "vehicle_model",
    align: "center",
    width: 300
  },
  {
    title: "产品名称",
    dataIndex: "product_name",
    align: "center",
    width: 300
  },
  {
    title: "客户品号",
    dataIndex: "product_cid",
    align: "center",
    width: 300,
  },
  {
    title: "产品总成号",
    dataIndex: "product_oid",
    align: "center",
    width: 300,
  },
  {
    title: "配套描述",
    dataIndex: "product_description",
    align: "center",
    width: 300,
  },
  {
    title: "申请时间",
    dataIndex: "application_time",
    align: "center",
    width: 300,
  },
  {
    title: "申请人",
    dataIndex: "applicant_name",
    align: "center",
    width: 300,
  }
];

const columnsImageApplication = [
    {
    title: "序号",
    dataIndex: "index",
    align: "center",
    width: 100,
    scopedSlots: { customRender: "index" }
  },
  {
    title: "客户",
    dataIndex: "customer_name",
    align: "center",
    width: 300
  },
  {
    title: "车型",
    dataIndex: "vehicle_model",
    align: "center",
    width: 300
  },
  {
    title: "产品名称",
    dataIndex: "product_name",
    align: "center",
    width: 300
  },
  {
    title: "客户品号",
    dataIndex: "product_cid",
    align: "center",
    width: 300,
  },
  {
    title: "产品总成号",
    dataIndex: "product_oid",
    align: "center",
    width: 300,
  },
  {
    title: "配套描述",
    dataIndex: "product_description",
    align: "center",
    width: 300,
  },
  {
    title: "申请时间",
    dataIndex: "application_time",
    align: "center",
    width: 300,
  },
  {
    title: "申请人",
    dataIndex: "applicant_name",
    align: "center",
    width: 300,
  },
  {
    title: "审核",
    dataIndex: "operation",
    align: "center",
    width: 300,
    scopedSlots: { customRender: "approve" }
  },
];


const columnsRulesOrg = [
    {
    title: "序号",
    dataIndex: "index",
    align: "center",
    width: 100,
    scopedSlots: { customRender: "index" }
  },
  {
    title: "产品分类代号",
    dataIndex: "product_cid",
    align: "center",
    width: 300
  },
  {
    title: "产品中文名称",
    dataIndex: "product_name_chn",
    align: "center",
    width: 300
  },
  {
    title: "产品英文名称",
    dataIndex: "product_name_en",
    align: "center",
    width: 300
  },
  {
    title: "类型",
    dataIndex: "product_type",
    align: "center",
    width: 300,
  },
  {
    title: "备注",
    dataIndex: "product_remarks",
    align: "center",
    width: 300,
  }
];

export default {
    components: {
        draggable,
        pdf
    },
    data() {
        return {
            // 图号搜索
            searchBarPlaceholder: "按图号搜索（产品总成号）",
            pageType: 1,
            hasQueried: false, // 图号搜索，是否已经进行搜索
            searchKeyword: undefined,
            searchType: undefined, // 搜索类型 1: 图号，2: 客户， 3: 车型，4:产品名称 5: 申请人，6: 产品类型，
            searchResultTab1: [],
            labelCol: { span: 5 },  
            wrapperCol: { span: 15 },
            confirmLoading: false,
            pagination: {}, //分页
            columnsImage: columnsImage,
            columnsImageQuery: columnsImage,
            columnsImageManage: columnsImage,
            columnsRules: columnsRulesOrg,
            columnsRulesOrg: columnsRulesOrg,
            columnsImageApplication: columnsImageApplication,
            autoCompeleteDict: {},
            autoSelectedRule: [],
            autoCompeleteKeyword: undefined,
            hasDimensionApply: false,
            hasAutoIncreaseApply: false,
            role: role,
            imageEdit: false,
            ruleEdit: false,
            ruleDetailHasDimension: false,
            ruleDetailHasSpec: false,

            // 申请
            imageId: undefined,
            ruleId: undefined,
            
            // 申请款
            imageApplication: false, // 图号申请弹框
            dataSource: [],
            value: '',
            applicationForm: this.$form.createForm(this, { name: 'applicationForm' }),
            
            // 台帐
            searchResultTab2: [],

            // 申请
            searchResultTab4: [],

            // 规则
            imageRuleAdd: false,
            searchResultTab3: [],
            ruleForm: this.$form.createForm(this, { name: 'ruleForm' })

        }
    },

    mounted() {
    },

    methods: {
        handleTableChange(pagination, filters, sorter) {//表格点击事件
            const pager = { ...this.pagination };
            pager.current = pagination.current;
            this.pagination = pager;
            const param = {
                sort_field: sorter.field,
                sort_order: sorter.order,
            }

            if (this.pageType == 1) {

            } else if (this.pageType == 2) {

            } else if (this.pageType == 3) {

            } else if (this.pageType == 4) {
                this.queryImageApplications()
            }

        },
        
        
        // 搜索类型 1: 图号，2: 客户， 3: 车型，4:产品名称 5: 申请人，6: 产品类型，

        searchByImageId() {
            this.searchBarPlaceholder = "按图号搜索（产品总成号）"
            this.searchType = 1
        },

        searchByProductName() {
            this.searchBarPlaceholder = "按产品名搜索"
            this.searchType = 4
        },

        searchByProductNameEnAndCHN() {
            this.searchBarPlaceholder = "按产品名搜索（中英文）"
            this.searchType = 4
        },

        searchByCustomerName() {
            this.searchBarPlaceholder = "按客户名搜索"
            this.searchType = 2
        },

        searchByVehicleModel() {
            this.searchBarPlaceholder = "按车型名称搜索"
            this.searchType = 3
        },

        searchByApplicant() {
            this.searchBarPlaceholder = "按申请人搜索"
            this.searchType = 5
        },

        searchByProductType() {
            this.searchBarPlaceholder = "按产品类型"
            this.searchType = 6
        },
        
        imageQuery() {
            this.pageType = 1
            this.searchBarPlaceholder = "按图号搜索（产品总成号）"
            this.searchType = 1
        },

        imageManage() {
            this.pageType = 2
            this.searchBarPlaceholder = "按产品名搜索"
            const tmpColumns = JSON.parse(JSON.stringify(this.columnsImage))
            if (this.role == "admin") {
                tmpColumns.push({
                    title: "操作",
                    dataIndex: "operation",
                    align: "center",
                    width: 300,
                    scopedSlots: { customRender: "operation" }
                })
            } 
            this.columnsImageManage = tmpColumns
            this.searchType = 4
            this.queryImages()
        },

        // 搜索类型 1: 图号，2: 客户， 3: 车型，4:产品名称 5: 申请人，6: 产品类型，
        queryImages() {
            const param = {}

            if (this.searchType == 2) {
                param.customer_name = this.searchKeyword
            } else if (this.searchType == 3) {
                param.vehicle_model = this.searchKeyword
            } else if (this.searchType == 4) {
                param.product_name = this.searchKeyword
            } else if (this.searchType == 5) {
                param.applicant_name = this.searchKeyword
            } else if (this.searchType == 1) {
                param.product_oid = this.searchKeyword
            }
            param.page = this.pagination.current || 1,
            ImageList(param)
                .then(res => {
                    if(res.code == '1'){
                        if (this.pageType == 1) {
                            this.searchResultTab1 = res.data.content;                        
                        } else {
                            this.searchResultTab2 = res.data.content;                        
                        }
                        const pagination = { ...this.pagination };
                        pagination.total = res.data.total_elements;
                        pagination.showTotal = () => `共${pagination.total}条数据`;
                        this.pagination = pagination;
                }})
                .catch(err => {});
        },

        imageRuleCreate() {
            this.pageType = 3
            this.searchBarPlaceholder = "按产品名搜索（中英文）"
            this.searchType = 4
            const tmpColumns = JSON.parse(JSON.stringify(this.columnsRulesOrg))
            if (this.role == "admin") {
                tmpColumns.push({
                    title: "操作",
                    dataIndex: "operation",
                    align: "center",
                    width: 300,
                    scopedSlots: { customRender: "operation" }
                })
            } 
            this.columnsRules = tmpColumns
            this.queryImageRules()
        },

        // 图号申请列表相关
        imageApplicationPage() {
            this.pageType = 4
            this.searchBarPlaceholder = "按产品名搜索"
            this.searchType = 4
            this.queryImageApplications()
        },

        // 搜索类型 1: 图号，2: 客户， 3: 车型，4:产品名称 5: 申请人，6: 产品类型，
        queryImageApplications() {
            const param = {}
            if (this.searchType == 2) {
                param.customer_name = this.searchKeyword
            } else if (this.searchType == 3) {
                param.vehicle_model = this.searchKeyword
            } else if (this.searchType == 4) {
                param.product_name = this.searchKeyword
            } else if (this.searchType == 5) {
                param.applicant_name = this.searchKeyword
            }
            param.page = this.pagination.current || 1,
            ImageApplications(param)
                .then(res => {
                    if(res.code == '1'){
                        this.searchResultTab4 = res.data.content;                        
                        const pagination = { ...this.pagination };
                        pagination.total = res.data.total_elements;
                        pagination.showTotal = () => `共${pagination.total}条数据`;
                        this.pagination = pagination;
                }})
                .catch(err => {});
        },

        resetImageQuery() {
            this.hasQueried = false;
            this.searchKeyword = undefined
            if (this.pageType == 4) {
                this.queryImageApplications()
            } else if (this.pageType == 3) {
                this.queryImageRules()
            } else if (this.pageType == 2) {
                this.queryImages()
            }
        },

        onSearchTab1() {
            this.hasQueried = true;
            this.queryImages()
        },

        // 除了第一个tab
        onSearchTab2() {
            if (this.pageType == 4) {
                this.queryImageApplications()
            } else if (this.pageType == 3) {
                this.queryImageRules()
            } else {
                this.queryImages()
            } 

        },

        enableImageApplication() {
            this.imageApplication = true;
        },

        enableImageRuleAdd() {
            this.imageRuleAdd = true;
        },

        // 提交申请
        handleImageApplicationOk() {
            this.applicationForm.validateFields((err, values) => {
                    const param = {
                        customer_name: values.customer_name,
                        product_cid: values.product_cid,
                        product_description: values.product_description,
                        product_name: values.product_name,
                        vehicle_model: values.vehicle_model,
                        product_rule_id: values.product_info.key,
                        applicant_username: Vue.ls.get("username"),
                        id: this.imageId
                    }
                    if (values.product_diameter) {
                        if (values.product_diameter > 100 || values.product_length > 100) {
                            this.$message.error("直径和长度需要小于100", 1)
                            return
                        }
                        param.product_diameter = values.product_diameter
                        param.product_length = values.product_length
                    }                    
                    ImageApply(param)
                    .then(resp => {
                        const code = resp.code
                        if (code == 1) {
                            if (this.imageEdit) {
                                this.$message.info("编辑成功", 1)
                            } else {
                                this.$message.info("申请成功", 1)
                            }
                            this.imageApplication = false;
                            this.autoSelectedRule = undefined
                            this.autoCompeleteDict = undefined
                            this.hasAutoIncreaseApply = false
                            this.hasDimensionApply = false
                            this.imageId = undefined
                            this.imageEdit = false
                            this.queryImages()
                            // 重新加载待审核数据
                            this.applicationForm.resetFields()
                        } else {
                            this.$message.error(resp.msg, 1)
                            
                        }
                    })
                    .catch(err => {})
                }).catch( err => {})
        },

        // 申请通过
        handleApplicationPass(record) {
            const that = this;
            this.$confirm({
                title: "提示",
                centered: true,
                okText: "确定",
                cancelText: "取消",
                content: "确认通过？",
                onOk() {
                    that.handleApplicationPassOk(record); // 删除
                },
                onCancel() {
                //that.visible = false;
                }
            });
        },

        handleApplicationPassOk(record) {
            const param = {
                application_id: record.id,
                audit_username: Vue.ls.get("username")
            }
            ImageApplicationPass(param)
                .then(resp => {
                    if (resp.code == 1) {
                        this.$message.info("审核成功", 1)
                        this.queryImageApplications()
                    } else {
                        this.$message.error("审核失败", 1)
                    }
                })
                .catch(err => {})

        },

        // 申请通过
        handleApplicationDeny(record) {
            const that = this;
            this.$confirm({
                title: "提示",
                centered: true,
                okText: "确定",
                cancelText: "取消",
                content: "确认审核通过？",
                onOk() {
                    that.handleApplicationDenyOk(record); // 删除
                },
                onCancel() {
                //that.visible = false;
                }
            });
        },

        handleApplicationDenyOk(record) {
            const param = {
                application_id: record.id,
                audit_username: Vue.ls.get("username")
            }
            ImageApplicationDeny(param)
                .then(resp => {
                    if (resp.code == 1) {
                        this.$message.info("审核成功", 1)
                        this.queryImageApplications()
                    } else {
                        this.$message.error("审核失败", 1)
                    }
                })
                .catch(err => {})

        },

        // 申请通过
        handleImageAddRuleOk() {
            this.ruleForm.validateFields((err, values) => {
                const param = {
                    id : this.ruleId,
                    product_cid: values.product_cid,
                    product_name_chn: values.product_name_chn,
                    product_name_en: values.product_name_en,
                    product_remarks: values.product_remarks,
                    product_type: values.product_type,
                    has_auto_increase: values.has_auto_increase ? 1: 0,
                    has_dimension: values.has_dimension ? 1: 0,
                    creator_username: Vue.ls.get("username")
                }
                AddImageRule(param)
                    .then(resp => {
                        const code = resp.code
                        if (code == 1) {
                            this.$message.info("新增成功", 1)
                            this.imageApplication = false;
                            this.ruleForm.resetFields()
                            this.imageRuleAdd = false
                            this.ruleDetailHasDimension = false
                            this.ruleDetailHasSpec = false 
                            this.ruleId = undefined
                            // 重新加载待审核数据
                            this.queryImageRules()
                        } else {
                            this.$message.error(resp.msg, 1)
                        }
                    })
                    .catch(err => {

                    })
                }).catch( err => {})
        },


        handleImageApplicationCancel() {
            this.imageApplication = false;
            this.dataSource = []
            this.autoCompeleteDict = {}
            this.autoCompeleteKeyword = undefined
            this.applicationForm.resetFields()
            this.imageEdit = false
        },


        handleImageAddRuleCancel() {
            this.ruleForm.resetFields()
            this.imageRuleAdd = false;
        },

        // 搜索类型 1: 图号，2: 客户， 3: 车型，4:产品名称 5: 申请人，6: 产品类型，
        queryImageRules() {
            const param = {}
            if (this.searchType == 4) {
                param.product_name = this.searchKeyword
            } else if (this.searchType == 6) {
                param.product_type = this.searchKeyword
            } 
            param.page = this.pagination.current || 1,
            ImageRuleList(param)
                .then(res => {
                    if(res.code == '1'){
                        this.searchResultTab3 = res.data.content;                        
                        const pagination = { ...this.pagination };
                        pagination.total = res.data.total_elements;
                        pagination.showTotal = () => `共${pagination.total}条数据`;
                        this.pagination = pagination;
                }})
                .catch(err => {});
        },

        // 删除规则
        handleDeleteRule(record) {
            const that = this
            const param = {
                rule_id: record.id,
                editor_username: Vue.ls.get("username")
            }
            this.$confirm({
                title: "提示",
                centered: true,
                okText: "确定",
                cancelText: "取消",
                content: "确认删除？",
                onOk() {
                    that.handleDeleteRuleOk(param); // 删除
                },
                onCancel() {
                //that.visible = false;
                }
            });
            
        },

        handleDeleteRuleOk(param) {
            DeleteImageRule(param)
                .then(resp => {
                    const code = resp.code
                        if (code == 1) {
                            this.$message.info("删除成功", 1)
                            this.queryImageRules()
                            // 重新加载待审核数据
                        } else {
                            this.$message.error(resp.msg, 1)
                            
                        }
                })
                .catch(err => {})
        },

        onSearchProductName(searchText) {
            this.autoCompeleteKeyword = undefined
            if (searchText.trim() != "") {
                const param = {
                    keyword: searchText
                }
                SearchRule(param)
                    .then(resp => {
                        if (resp.code == 1) {
                            this.dataSource = resp.data
                            const tmp_dict = {}
                            for (var i = 0; i < this.dataSource.length; i++) {
                                tmp_dict[this.dataSource[i].id] = this.dataSource[i]
                            }
                            this.autoCompeleteDict = tmp_dict
                        } else {
                            this.$message.error(resp.msg, 1)
                        }
                    })
                    .catch(err => {
                    })
            } else {
                this.dataSource = []
                this.autoCompeleteDict = {}
            }
            // this.dataSource = !searchText ? [] : [searchText, searchText.repeat(2), searchText.repeat(3)];
        },
        onSelectProductName(value) {
            const key = value.key
            this.hasDimensionApply = this.autoCompeleteDict[key].has_dimension == 1 ? true: false
            this.hasAutoIncreaseApply = this.autoCompeleteDict[key].has_dimension == 1 ? true: false
            
        },
        onChange(value)  {
            this.autoCompeleteKeyword = value.label
        },

        handleImageEdit(record) {
            this.imageRuleAdd = true
            this.imageEdit = true
            this.queryImageDetail(record)

        },

        queryImageDetail(record) {
            const param = {
                image_id: record.id
            }
            ImageDetail(param)
                .then(resp => {
                    if (resp.code == 1) {
                        const product_info = {key: resp.data.product_rule_id, label: resp.data.show_name}
                        this.hasDimensionApply = resp.data.has_dimension == 1? true:false
                        const detail = {
                            customer_name: resp.data.customer_name,
                            vehicle_model: resp.data.vehicle_model,
                            product_name: resp.data.product_name,
                            product_info: product_info,
                            product_cid: resp.data.product_cid,
                            product_description: resp.data.product_description,
                            product_length: resp.data.product_length,
                            product_diameter: resp.data.product_diameter
                        }
                        this.imageId = resp.data.id
                        this.imageApplication = true
                        this.$nextTick(() => {  
                            this.applicationForm.setFieldsValue(detail)
                        });
                    }
                })
                .catch(err => {})
        },

        handleRuleEdit(record) {
            this.ruleEdit = true
            this.imageRuleAdd = true
            this.queryRuleDetail(record)
        },

        queryRuleDetail(record) {
            const param = {
                rule_id: record.id
            }
            RuleDetail(param)
                .then(resp => {
                    if (resp.code == 1) {
                        const detail = {
                            old_product_cid: resp.data.product_cid,
                            old_product_name_chn: resp.data.product_name_chn,
                            product_cid: resp.data.product_cid,
                            product_name_chn: resp.data.product_name_chn,
                            product_name_en: resp.data.product_name_en,
                            product_type: resp.data.product_type,
                            product_remarks: resp.data.product_remarks,
                            has_dimension: resp.data.has_dimension == 1 ? true : false,
                            has_auto_increase: resp.data.has_auto_increase == 1 ? true : false,
                        }
                        this.ruleDetailHasDimension = resp.data.has_dimension == 1 ? true : false
                        this.ruleDetailHasSpec = resp.data.has_auto_increase == 1 ? true : false
                        this.ruleId = resp.data.id
                        this.$nextTick(() => {  
                            this.ruleForm.setFieldsValue(detail)
                        });
                    }
                })
                .catch(err => {})
        },



        handleDeleteImage(record) {
            const that = this
            const param = {
                image_id: record.id,
                editor_username: Vue.ls.get("username")
            }
            this.$confirm({
                title: "提示",
                centered: true,
                okText: "确定",
                cancelText: "取消",
                content: "确认删除？",
                onOk() {
                    that.handleDeleteImageOk(param); // 删除
                },
                onCancel() {
                //that.visible = false;
                }
            });
            
        },

        handleDeleteImageOk(param) {
            ImageDelete(param)
                .then(resp => {
                    const code = resp.code
                        if (code == 1) {
                            this.$message.info("删除成功", 1)
                            this.queryImages()
                            // 重新加载待审核数据
                        } else {
                            this.$message.error(resp.msg, 1)
                            
                        }
                })
                .catch(err => {

                })
        }   

        
    },
    computed:  {
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
    margin: 12px 12px;

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

.search-selection {
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
