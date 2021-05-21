/* 车辆管理 */
import {axios} from '@/utils/request'

const api = {
    carlist: '/share-parking/web/car/list', //查询车辆list
}

export default api

export function carlist(parma) {
  return axios({
    url: api.carlist,
    method: 'post',
    data: parma //params
  })
}