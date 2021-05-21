import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import '@/assets/styles/reset.css'
import "@/assets/font/font.css"
import {
  LocaleProvider,
  Form,
  ConfigProvider,
  Menu,
  Card,
  Row,
  Col,
  Modal,
  Tabs,
  Descriptions,
  Carousel,
  TreeSelect,
  Progress,
  Button,
  Checkbox,
  Radio,
  Tag,
  Collapse,
  List,
  Steps,
  Select,
  DatePicker,
  Input,
  Icon,
  Switch,
  TimePicker,
  Table,
  Breadcrumb,
  Popconfirm,
  Spin,
  Notification,
  Layout,
  Avatar,
  Dropdown,
  message,
  Upload,
  AutoComplete
} from "ant-design-vue";

Vue.use(LocaleProvider);
Vue.use(Form);
Vue.use(Menu);
Vue.use(Card);
Vue.use(Row);
Vue.use(Col);
Vue.use(Modal);
Vue.use(Tabs);
Vue.use(Descriptions);
Vue.use(Carousel);
Vue.use(TreeSelect);
Vue.use(Progress);
Vue.use(Button);
Vue.use(ConfigProvider);
Vue.use(Checkbox);
Vue.use(Collapse);
Vue.use(Tag);
Vue.use(List);
Vue.use(Steps);
Vue.use(Select);
Vue.use(DatePicker);
Vue.use(Input);
Vue.use(Icon);
Vue.use(Switch);
Vue.use(TimePicker);
Vue.use(Table);
Vue.use(Breadcrumb);
Vue.use(Popconfirm);
Vue.use(Spin);
Vue.use(Notification);
Vue.use(Layout);
Vue.use(Avatar);
Vue.use(Dropdown);
Vue.use(Radio);
Vue.use(Upload);
Vue.use(AutoComplete);
Vue.config.productionTip = false
Vue.prototype.$confirm = Modal.confirm
Vue.prototype.$message = message; //提示框
Vue.prototype.$Modal = Modal; //确认提示框
// Vue.prototype.$notification = notification
// Vue.prototype.$info = Modal.info
// Vue.prototype.$success = Modal.success
// Vue.prototype.$error = Modal.error
// Vue.prototype.$warning = Modal.warning

import VueStorage from "vue-ls";
const storageOptions = {
  namespace: "pro__", // // key键前缀
  name: "ls", // // 命名Vue变量.[ls]或this.[$ls],
  storage: "local" // 存储名称: session, local, memory
};
Vue.use(VueStorage, storageOptions);

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  render: h => h(App)
})
