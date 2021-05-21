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
              <label class="serch-item-text">车牌号码</label>
              <a-input
                class="serch-item-input"
                placeholder="车场名称"
                v-model="plateNo"
              />
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
              <label class="serch-item-text">车位组</label>
              <a-input
                class="serch-item-input"
                placeholder="车场名称"
              />
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
              <label class="serch-item-text">车主姓名</label>
              <a-input
                class="serch-item-input"
                placeholder="车主姓名"
                v-model="ownerName"
              />
            </a-col>
          </a-row>
          <a-row
            class="table-serch"
            :gutter="{ xs: 8, sm: 16, md: 8, lg: 6 }"
            type="flex"
            style="margin:0;margin-top:20px;"
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
              <label class="serch-item-text">车主电话</label>
              <a-input
                class="serch-item-input"
                placeholder="车主电话"
                v-model="ownerPhone"
              />
            </a-col>
            <a-col
              class="gutter-row"
              :span="4"
              :xs="24"
              :sm="12"
              :md="12"
              :lg="6"
              :xl="6"
            >
              <label class="serch-item-text">车&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;型</label>
              <a-select
                class="serch-item-input"
                placeholder="请选择"
                v-model="carType"
              >
                <a-select-option key="">
                  请选择
                </a-select-option>
                <a-select-option key="1">
                  小型车
                </a-select-option>
                <a-select-option key="2">
                  大型车
                </a-select-option>
                <a-select-option key="3">
                  超大型车
                </a-select-option>
              </a-select>
            </a-col>
            <a-col
              class="gutter-row"
              :span="4"
              :xs="24"
              :sm="12"
              :md="12"
              :lg="6"
              :xl="6"
            >
              <label class="serch-item-text">车&nbsp;&nbsp;&nbsp;&nbsp;类</label>
              <a-select
                class="serch-item-input"
                placeholder="请选择"
                v-model="chargeType"
              >
                <a-select-option key="">
                  请选择
                </a-select-option>
                <a-select-option key="0">
                  固定车
                </a-select-option>
                <a-select-option key="1">
                  月租
                </a-select-option>
                <a-select-option key="3">
                  临时停车
                </a-select-option>
              </a-select>
            </a-col>
            <a-col class="gutter-row" style="padding-right:0">
              <a-button
                type="primary"
                class="serch-btn tool-btn"
                @click="preQueryRecords()"
                >查询</a-button>
                <a-button >导入</a-button>
                <a-button >导出</a-button>
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
import {carlist} from '@/api/vehicleinformation'
import {parkinglist} from '@/api/depotmanagement'
import { mapState } from "vuex";
const columns = [
  {
    title: "所属车场",
    dataIndex: "parkingName",
    align: "center",
    width: 200
  },
  {
    title: "车型",
    dataIndex: "carType",
    align: "center",
    width: 200,
    customRender: function(val, item, rowIndex) {
      if (val == 1) {
        return "小型车";
      } else if (val && val == 2) {
        return "大型车";
      } else if(val && val== 3){
        return '超大型车'
      }
    }
  },
  {
    title: "车类",
    dataIndex: "chargeType",
    align: "center",
    width: 200,
    customRender: function(val, item, rowIndex) {
      if (val == 0) {
        return "固定车";
      } else if (val && val == 1) {
        return "月租";
      } else if(val && val== 3){
        return '临时停车'
      }
    }
  },
  {
    title: "车牌号",
    dataIndex: "plateNo",
    align: "center",
    width: 200
  },
  {
    title: "车辆颜色",
    dataIndex: "carColor",
    align: "center",
    width: 200
  },
  {
    title: "车位组",
    dataIndex: "",
    align: "center",
    width: 200
  },
  {
    title: "车主姓名",
    dataIndex: "ownerName",
    align: "center",
    width: 200
  },
  {
    title: "车主电话",
    dataIndex: "ownerPhone",
    align: "center",
    width: 200
  },
  {
    title: "详细地址",
    dataIndex: "ownerAddress",
    align: "center",
    width: 200
  }
];
export default {
  name: "Channelmanagement",
  components: {},
  data() {
    return {
      communityCode:this.$store.state.user.communityCode, //所属社区
      parkingCode:"",//停车场编号
      plateNo:"",//车牌号
      ownerName:"",
      ownerPhone:"",
      carType:"",
      chargeType:"",//车辆类型，0固定车，1月租车
      dwList: [], //车场
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
    handleTableChange(pagination, filters, sorter) {//表格点击事件
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;
      this.carlist(); //查询列表
    },    
    preQueryRecords() {
      //查询
      const pager = { ...this.pagination };
      pager.current = 1;
      this.pagination = pager;
      this.carlist();
    },
    carlist() {
      // 列表接口
      var parma = {
        pageInfo:{
          pageNumber: this.pagination.current || 1,
          pageSize: 10,
        },
        communityCode: this.communityCode,
        parkingCode: this.parkingCode,
        plateNo: this.plateNo,
        ownerName: this.ownerName,
        ownerPhone: this.ownerPhone,
        carType:this.carType,
        chargeType:this.chargeType
      };
      carlist(parma)
        .then(res => {
          this.data = res.data.content;
          const pagination = { ...this.pagination };
          pagination.total = res.data.totalElements;
          pagination.showTotal = () => `共${res.data.totalElements}条数据`;
          this.pagination = pagination;
        })
        .catch(err => {});
    }
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
    width: 60%;
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
