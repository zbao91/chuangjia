/* 通道管理 */
import {axios} from '@/utils/request'

const api = {
    passagelist: '/share-parking/web/passage/list', //查询通道list
}

export default api

export function passagelist(parma) {
  return axios({
    url: api.passagelist,
    method: 'post',
    data: parma //params
  })
}