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
              :span="3"
              :xs="24"
              :sm="12"
              :md="12"
              :lg="6"
              :xl="6"
            >
              <label class="serch-item-text">所属车场</label>
              <a-select
                style="width:63%"
                class="serch-item-input"
                placeholder="请选择"
                v-model="parkingCode"
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
              :span="3"
              :xs="24"
              :sm="12"
              :md="12"
              :lg="6"
              :xl="6"
            >
              <label class="serch-item-text">时间</label>
              <a-range-picker
                  allowClear
                  class="serch-item-input"
                  format="YYYY-MM-DD"
                  @change='onTimechange'
                />
            </a-col>
            <a-col class="gutter-row" style="padding-right:0">
              <a-button
                type="primary"
                class="serch-btn tool-btn"
                @click="preQueryRecords()"
                >查询</a-button>
            </a-col>
          </a-row>
        </div>
      </a-card>
      <a-card style="margin-top: 16px;">
        <a-table
          :columns="columns"
          :dataSource="data"
          :pagination="pagination"
          @change="handleTableChange"
        >
        </a-table>
      </a-card>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import {Summarylist} from '@/api/vehiclesummary'
import {parkinglist} from '@/api/depotmanagement'
const columns = [
  {
    title: "车场名称",
    dataIndex: "parkingName",
    align: "center",
    width: 200
  },
  {
    title: "通道名称",
    dataIndex: "passName",
    align: "center",
    width: 200
  },
  {
    title: "进场次数",
    dataIndex: "entryNum",
    align: "center",
    width: 200
  },
  {
    title: "出场次数",
    dataIndex: "outNum",
    align: "center",
    width: 200
  }
];
export default {
  name: "Vehiclesummary",
  components: {},
  data() {
    return {
      communityCode:this.$store.state.user.communityCode, //所属社区
      parkingCode:"",
      publishDateBegin:'',//开始时间
      publishDateEnd:'',//结束时间
      deptIds: "", //所属社区
      dwList: [], //所属停车场
      formCompany: this.$form.createForm(this),
      columns,
      data: [], //表格数据显示
      pagination: {}, //分页
      record: {}
    };
  },

  mounted() {
    this.parkinglist() //停车场下拉列表
    this.preQueryRecords() //查询列表
  },

  methods: {
    handleTableChange(pagination, filters, sorter) {//表格点击事件
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;
      this.queryRecords(); //查询列表
    }, 
    parkinglist() { //停车场下拉列表
      // 列表接口
      var parma = {
        pageInfo:{
          pageNumber: 1,
          pageSize: 1000,
        },
        communityCode:this.communityCode,
      };
      parkinglist(parma)
        .then(res => {
          const data = res.data.content;
          this.dwList=data.map((item,index)=>{
            return {id:item.parkingCode,deptName:item.parkingName}
          })

        })
        .catch(err => {});
    },
    onTimechange(dates, dateStrings) { //时间
      this.publishDateBegin=dateStrings[0]
      this.publishDateEnd=dateStrings[1] 
    },
    preQueryRecords() {
      //查询
      const pager = { ...this.pagination };
      pager.current = 1;
      this.pagination = pager;
      this.queryRecords();
    },
    queryRecords() {
      // 列表接口
      var parma = {
        pageInfo:{
          pageNumber: this.pagination.current || 1,
          pageSize: 10,
        },
        communityCode: this.communityCode,
        parkingCode: this.parkingCode,
        startTime: this.publishDateBegin?this.publishDateBegin+" 00:00:00":"",
        endTime: this.publishDateEnd?this.publishDateEnd+" 23:59:59":"",
      };
      Summarylist(parma)
        .then(res => {
          this.data = res.data.content;
          const pagination = { ...this.pagination };
          pagination.total = res.data.totalElements;
          pagination.showTotal = () => `共${res.data.totalElements}条数据`;
          this.pagination = pagination;
        })
        .catch(err => {});
    },
    // rest() {
    //   //清空查询条件
    //   this.departmentName = "";
    // }
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
