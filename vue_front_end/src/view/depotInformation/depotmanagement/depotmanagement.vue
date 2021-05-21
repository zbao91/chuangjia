<template>
  <div>
    <div class="tabsList">
      <a-card>
        <div class="table-serch">
          <a-row
            class="table-serch"
            :gutter="{ xs: 8, sm: 16, md: 8, lg: 6 }"
            type="flex"
            justify="space-between"
            style="margin:0"
          >
            <a-col
              class="gutter-row"
              :span="6"
              :xs="24"
              :sm="12"
              :md="12"
              :lg="7"
              :xl="7"
            >
              <label class="serch-item-text">所属单位</label>
              <a-select
                style="width:230px"
                class="serch-item-input"
                placeholder="请选择"
                v-model="unitCode"
              >
                <a-select-option key="">
                  请选择
                </a-select-option>
                <a-select-option v-for="key in dwList" :key="key.id">
                  {{ key.deptName }}
                </a-select-option>
              </a-select>
            </a-col>
            <a-col
              class="gutter-row"
              :span="6"
              :xs="24"
              :sm="12"
              :md="12"
              :lg="7"
              :xl="7"
            >
              <label class="serch-item-text">车场名称</label>
              <a-input
                class="serch-item-input"
                placeholder="车场名称"
                v-model="parkingName"
              />
            </a-col>
            <a-col class="gutter-row" style="padding-right:0">
              <!-- <a-button  @click="rest()">重置</a-button> -->
              <a-button
                type="primary"
                class="serch-btn tool-btn"
                @click="preQueryRecords()"
                >查询</a-button
              >
            </a-col>
          </a-row>
        </div>
      </a-card>
      <a-card style="margin-top: 16px;">
        <div style="text-align:right;margin-bottom:20px;">
          <a-button
            type="primary"
            class="serch-btn tool-btn"
            @click="add()"
            style="margin-left:16px"
            >新增</a-button
          >
        </div>
        <a-table
          :columns="columns"
          :dataSource="data"
          :pagination="pagination"
          @change="handleTableChange"
        >
          <template slot="operation" slot-scope="text, record">
            <div class="editable-row-operations">
              <a class="tool-table" @click="xiugai(record)">修改</a>
              <a class="tool-table" @click="shanchu(record)">刪除</a>
            </div>
          </template>
        </a-table>
      </a-card>
    </div>

    <a-modal
      :title="title"
      v-model="visible"
      @ok="handleOk"
      @cancel="handleCancel"
    >
      <a-form :form="formCompany">
        <a-form-item
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          label="所属单位"
        >
          <a-select
            :disabled="!isadd"
            v-decorator="[
              'unitCode',
              { rules: [{ required: true, message: '请选择所属单位!' }] }
            ]"
            placeholder="选择"
          >
            <a-select-option v-for="(item,index) in dwList" :key="index" :value="item.id">
              {{item.deptName}}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          label="所属社区"
        >
          <a-select
            v-decorator="[
              'communityCode',
              { rules: [{ required: true, message: '请选择所属社区!' }] }
            ]"
            placeholder="选择"
          >
            <a-select-option v-for="(item,index) in sqlist" :key="index" :value="item.id">
              {{item.name}}
            </a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          label="车场名称："
        >
          <a-input
            v-decorator="[
              'parkingName',
              {
                rules: [
                  {
                    required: true,
                    message: '请输入车场名称!',
                    whitespace: true
                  }
                ]
              }
            ]"
            placeholder="车场名称："
          />
        </a-form-item>
        <a-form-item
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          label="车场地址："
        >
          <a-textarea
            :rows="3"
            v-decorator="['parkingAddress']"
            placeholder="请输入车场地址"
          ></a-textarea>
        </a-form-item>
        <a-form-item
          :label-col="{ span: 6 }"
          :wrapper-col="{ span: 16 }"
          label="收费标准"
        >
          <a-input
            v-decorator="[
              'feeScale',
              {
                rules: [
                  {
                    required: true,
                    message: '请输入收费标准!',
                    whitespace: true
                  }
                ]
              }
            ]"
            placeholder="收费标准"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import Vue from "vue";
import { mapState } from "vuex";
import {parkinglist, parkingadd, parkingediter,parkingdelete} from '@/api/depotmanagement'
import {companylist} from '@/api/company'
const columns = [
  {
    title: "所属单位",
    dataIndex: "unitName",
    align: "center",
    width: 200
  },
  {
    title: "车场编号",
    dataIndex: "parkingCode",
    align: "center",
    width: 200
  },
  {
    title: "车场名称",
    dataIndex: "parkingName",
    align: "center",
    width: 200
  },
    {
    title: "车场地址",
    dataIndex: "parkingAddress",
    align: "center",
    width: 200
  },
  {
    title: "收费标准",
    dataIndex: "feeScale",
    align: "center",
    width: 200
  
  },
  {
    title: "操作",
    align: "center",
    width: 200,
    scopedSlots: { customRender: "operation" }
  }
];
export default {
  name: 'Depotmanagement',
  components: {},
  data() {
    return {
      communityCode:this.$store.state.user.communityCode, //所属社区
      parkingName:"",//停车场名称
      unitCode:"",//所属单位
      sqlist:[
        {
          id: '111',
          name: "东信社区"
        }
      ],
      dwList: [], //所属单位
      visible: false,
      isadd:true, //是否新增是true:新增  false:修改
      title: "新增",

      formCompany: this.$form.createForm(this),
      columns,
      data: [], //表格数据显示
      pagination: {}, //分页
      record: {}
    };
  },
  mounted() {
    this.preQueryRecords() //查询列表
  this.companylist() //列表
  },

  methods: {
    handleTableChange(pagination, filters, sorter) {//表格点击事件
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;
      this.parkinglist(); //查询列表
    },
    companylist() {
      // 列表接口
      var parma = {
        communityCode:this.communityCode,
        pageInfo:{
          pageNumber: 1,
          pageSize:1000
        }
      };
      companylist(parma)
        .then(res => {
          if(res.code=='0'){
            const data = res.data.content;
            this.dwList=data.map((item,index)=>{
              return {id:item.unitCode,deptName:item.unitName}
            })
          }
        })
        .catch(err => {});
    },
    preQueryRecords() {
      //查询
      const pager = { ...this.pagination };
      pager.current = 1;
      this.pagination = pager;
      this.parkinglist();
    },
    parkinglist() {
      // 列表接口
      var parma = {
        pageInfo:{
          pageNumber: this.pagination.current || 1,
          pageSize: 10,
        },
        communityCode:this.communityCode,
        unitCode: this.unitCode,
        parkingName: this.parkingName
      };
      parkinglist(parma)
        .then(res => {
          this.data = res.data.content;
          const pagination = { ...this.pagination };
          pagination.total = res.data.totalElements;
          pagination.showTotal = () => `共${res.data.totalElements}条数据`;
          this.pagination = pagination;
        })
        .catch(err => {});
    },
    rest() {
      //清空查询条件
      this.departmentName = "";
    },
    add() {
      //新增
      this.title = "新增";
      this.isadd=true
      this.visible = true;
      this.formCompany.resetFields(); //置空表单
    },
    xiugai(record) {
      //修改
      this.title = "修改";
      this.isadd=false
      this.visible = true;
      this.formCompany.resetFields();
      this.record = {
        ...record
      };
      this.$nextTick(() => {
        this.formCompany.setFieldsValue(record);
      });
    },
    shanchu(record) {
      //删除
      const that = this;
      this.$confirm({
        title: "提示",
        centered: true,
        okText: "确定",
        cancelText: "取消",
        content: "确认删除？",
        onOk() {
          that.handleDeleteOk(record); //删除
        },
        onCancel() {
          //that.visible = false;
        }
      });
    },
    handleDeleteOk(record) {
      //删除接口
      const parm={communityCode:this.communityCode,parkingCode:record.parkingCode}
      parkingdelete(parm)
        .then(res => {
          if (res.code == "0") {
            this.$message.success('删除成功！', 3);
            this.preQueryRecords();
          } else {
            this.$message.warning('删除失败！', 3);
          }
        })
        .catch(err => {});
    },
    handleOk() {
      //保存
      this.saveOrUpdate();
    },
    handleCancel() {
      //取消
      this.visible = false;
    },
    saveOrUpdate() {
      //新增和修改共用
      var param = {};
      const that=this
      this.formCompany.validateFields((errors, values) => {
        if (!errors) {
          param = {
            communityCode: values.communityCode,
            parkingName: values.parkingName,//车场名称
            address: values.parkingAddress,//车场地址
            feeScale: values.feeScale, //收费标准
            unitCode:values.unitCode,
          };
          if (that.isadd==true) {
            this.parkingadd(param)
          }else{
            param.parkingCode = that.record.parkingCode;
            this.parkingediter(param)
          }
        }
      });
    },
    parkingadd(param){//添加
      parkingadd(param).then(res => {
        if (res.code == "0") {
          this.visible = false;
          this.$message.success('添加成功！', 3);
          this.preQueryRecords(); //查询列表
        } else {
          //验证码输入错误
          this.$message.warning(res.msg, 3);
        }
      });
    },
    parkingediter(param){//修改
      parkingediter(param).then(res => {
        if (res.code == "0") {
          this.visible = false;
          this.$message.success('修改成功！', 3);
          this.preQueryRecords(); //查询列表
        } else {
          //验证码输入错误
          this.$message.warning(res.msg, 3);
        }
      });
    },
  }
};
</script>
<style lang="less" scoped>
.tabsList {
  &/deep/.ant-tabs-nav-wrap {
    background: #ffffff;
  }
  &/deep/.ant-tabs-bar {
    margin: 0 0 1px 0;
    border-bottom: none;
  }
  .tabs-list {
    height: 30px;
    margin-bottom: 20px;
    background: #ffffff;
    &/deep/.ant-tabs-nav-container {
      border-bottom: 1px solid #e8e8e8 !important;
      background: #ffffff !important;
    }
    .list-item {
      cursor: pointer;
      display: inline-block;
      background: #ffffff;
      height: 30px;
      line-height: 30px;
      border: 1px solid #e8e8e8 !important;
      border-right: none;
      padding: 0 5px;
    }

    .list-active {
      background: #e8e8e8;
    }
  }
  .table-serch {
    display: flex;
    width: 100%;
    flex-wrap: wrap;
  }

  .serch-item {
    display: flex;
    min-width: 300px;
    align-items: center;
  }

  .serch-item-input {
    margin-left: 16px;
    width: 200px;
  }

  .serch-btn {
    margin-left: 24px;
  }

  .add-btn {
    margin-left: 16px;
  }

  .tool-table {
    margin: 16px;
  }

  .liner1-first {
    width: 400px;
    display: flex;
    align-items: center;
  }

  .liner1-other {
    width: 400px;
    display: flex;
    margin-top: 16px;
    align-items: center;
  }

  .liner1-left-txt {
    min-width: 100px;
    width: 100px;
    color: rgba(0, 0, 0, 0.85);
  }
}
</style>
