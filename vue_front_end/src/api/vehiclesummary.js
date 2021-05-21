/* 车辆进出 */
import {axios} from '@/utils/request'

const api = {
    Summarylist: '/share-parking/web/operation/listSummary', //查询车辆进出汇总list
}

export default api

export function Summarylist(parma) {
  return axios({
    url: api.Summarylist,
    method: 'post',
    data: parma //params
  })
}