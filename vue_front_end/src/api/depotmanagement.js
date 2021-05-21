/* 车场信息 */
import {axios} from '@/utils/request'

const api = {
  parkinglist: '/share-parking/web/parking/list', //查询车场list
  parkingadd:'/share-parking/web/parking/add', //新增
  parkingediter:'/share-parking/web/parking/update',//修改
  parkingdelete:'/share-parking/web/parking/delete',//删除
}

export default api

export function parkinglist(parma) {
  return axios({
    url: api.parkinglist,
    method: 'post',
    data: parma //params
  })
}
export function parkingadd(parma) {
    return axios({
      url: api.parkingadd,
      method: 'post',
      data: parma //params
    })
  }
  export function parkingediter(parma) {
    return axios({
      url: api.parkingediter,
      method: 'post',
      data: parma //params
    })
  }
  export function parkingdelete(parma) {
    return axios({
      url: api.parkingdelete,
      method: 'get',
      params: parma //params
    })
  }