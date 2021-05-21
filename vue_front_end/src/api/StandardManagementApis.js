import {axios} from '@/utils/request'

export function CreateFolder(parameter) {//创建文件夹分类
  return axios({
    url: 'standard/create_folder',
    method: 'post',
    params: parameter
  })
}


export function QueryFolderList(parameter) {//获取目录列表
  return axios({
    url: 'standard/folder_list',
    method: 'get',
    params: parameter
  })
}


export function StandardFileList(parameter) {//获取文件列表
  return axios({
    url: 'standard/file_list',
    method: 'get',
    params: parameter
  })
}


export function DeleteStandard(parameter) {//删除文件
  return axios({
    url: 'standard/delete_file',
    method: 'post',
    params: parameter
  })
}

export function CreateStandard(parameter) {//创建标准
  return axios({
    url: 'standard/create_standard',
    method: 'post',
    params: parameter
  })
}

export function FileDetail(parameter) {//标准详情
  return axios({
    url: 'standard/file_detail',
    method: 'get',
    params: parameter
  })
}


export function FolerEdit(parameter) {//目录修改
  return axios({
    url: 'standard/edit_folder',
    method: 'post',
    params: parameter
  })
}

export function FolderDelete(parameter) {//删除目录
  return axios({
    url: 'standard/delete_folder',
    method: 'post',
    params: parameter
  })
}


