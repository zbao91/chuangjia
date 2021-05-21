/* 车辆进出记录 */
import {axios} from '@/utils/request'

const api = {
    caroutlist: '/share-parking/web/operation/list', //查询车辆list
}

export default api

export function caroutlist(parma) {
  return axios({
    url: api.caroutlist,
    method: 'post',
    data: parma //params
  })
}