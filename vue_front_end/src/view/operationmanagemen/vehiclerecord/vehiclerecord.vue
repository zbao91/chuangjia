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
                placeholder="车牌号码"
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
              <label class="serch-item-text">姓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;名</label>
              <a-input
                class="serch-item-input"
                placeholder="姓名"
                v-model="ownerName"
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
              <label class="serch-item-text">电&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;话</label>
              <a-input
                class="serch-item-input"
                placeholder="电话"
                v-model="ownerPhone"
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
              <label class="serch-item-text">车位组&nbsp;&nbsp;&nbsp;&nbsp;</label>
              <a-input
                class="serch-item-input"
                placeholder="车位组"
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
              <label class="serch-item-text">车&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;类</label>
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
            <a-col
              class="gutter-row"
              :span="3"
              :xs="24"
              :sm="12"
              :md="12"
              :lg="6"
              :xl="6"
            >
              <label class="serch-item-text">入场通道</label>
              <a-input
                class="serch-item-input"
                placeholder="入场通道"
                v-model="entryName"
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
              <label class="serch-item-text">出场通道</label>
              <a-input
                class="serch-item-input"
                placeholder="出场通道"
                v-model="outName"
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
              <label class="serch-item-text">时间类型</label>
              <a-select
                class="serch-item-input"
                placeholder="请选择"
                v-model="timeType"
              >
                <!-- <a-select-option key="">
                  请选择
                </a-select-option>
                <a-select-option v-for="key in dwList" :key="key.id">
                  {{ key.deptName }}
                </a-select-option> -->
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
              <label class="serch-item-text">时间范围</label>
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
import {caroutlist} from '@/api/vehiclerecord'
import {parkinglist} from '@/api/depotmanagement'
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
    title: "入场通道",
    align: "center",
    dataIndex:"entryName",
    width: 200
  },
  {
    title: "出场通道",
    align: "center",
    dataIndex:"outName",
    width: 200
  },
  {
    title: "入场时间",
    dataIndex: "arriveTime",
    align: "center",
    width: 200
  },
  {
    title: "出场时间",
    dataIndex: "endTime",
    align: "center",
    width: 200
  },
  {
    title: "停车时长",
    dataIndex: "duration",
    align: "center",
    width: 200
  }
];
export default {
  name: "Vehiclerecord",
  components: {},
  data() {
    return {
      communityCode:this.$store.state.user.communityCode, //所属社区
      parkingCode:"",//所属车场
      plateNo:"",
      ownerName:"",
      ownerPhone:"",
      chargeType:"",
      carType:"",
      entryName:"",
      outName:"",
      timeType:"",
      startTime:"",
      endTime:"",
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
    onTimechange(dates, dateStrings) { //时间范围
      this.startTime=dateStrings[0]
      this.endTime=dateStrings[1] 
    },
    handleTableChange(pagination, filters, sorter) {//表格点击事件
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;
      this.queryRecords(); //查询列表
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
        communityCode:this.communityCode,
        pageInfo:{
          pageNumber: this.pagination.current || 1,
          pageSize: 10,
        },
        parkingCode:this.parkingCode,//所属车场
        plateNo:this.plateNo,
        ownerName:this.ownerName,
        ownerPhone:this.ownerPhone,
        chargeType:this.chargeType,
        carType:this.carType,
        entryName:this.entryName,
        outName:this.outName,
        timeType:this.timeType,
        value:"",
        startTime:this.startTime?this.startTime+" 00:00:00":"",
        endTime:this.endTime?this.endTime+" 23:59:59":"",
      };
      caroutlist(parma)
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
