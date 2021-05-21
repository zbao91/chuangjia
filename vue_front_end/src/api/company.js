/* 单位管理 */
import { axios } from "@/utils/request";

const api = {
  companylist: "/share-parking/web/unit/list", //查询单位信息
  companyadd: "/share-parking/web/unit/add", //新增
  companyediter: "/share-parking/web/unit/update", //修改
  companydelete: "/share-parking/web/unit/delete" // 删除
};

export default api;

export function companylist(parma) {
  return axios({
    url: api.companylist,
    method: "post",
    data: parma //params
  });
}
export function companyadd(parma) {
  return axios({
    url: api.companyadd,
    method: "post",
    data: parma //data
  });
}

export function companyediter(parma) {
  return axios({
    url: api.companyediter,
    method: "post",
    data: parma //data
  });
}

export function companydelete(parma) {
  return axios({
    url: api.companydelete,
    method: "get",
    params: parma //data
  });
}