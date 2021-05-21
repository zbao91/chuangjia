import {axios} from '@/utils/request'

export function createFolderCategory(parameter) {//创建文件夹分类
  return axios({
    url: 'files/create_folder_category',
    method: 'post',
    params: parameter
  })
}

export function getCategorFolderList(parameter) {//文件列表
  return axios({
    url: 'files/folder_list',
    method: 'get',
    params: parameter
  })
}

export function getCategoryList() {// 文件分类列表
    return axios({
      url: 'files/category_list',
      method: 'get',
    })
}

export function createCategory(parameter) {// 文件分类列表
  return axios({
    url: 'files/create_category',
    method: 'post',
    params: parameter
  })
}

export function createFolder(parameter) {// 文件分类列表
  return axios({
    url: 'files/create_folder',
    method: 'post',
    params: parameter
  })
}

export function updateCategoryAndFolder(parameter) {// 文件分类列表
  return axios({
    url: 'files/update_category_folder',
    method: 'post',
    params: parameter
  })
}

export function getFileList(parameter) {// 文件列表
  return axios({
    url: 'files/file_list',
    method: 'get',
    params: parameter
  })
}

export function uploadFiles(parameter) {// 文件列表
  return axios({
    url: 'files/upload_files',
    method: 'post',
    params: parameter
  })
}


export function deleteFile(parameter) {// 文件列表
  return axios({
    url: 'files/delete_file',
    method: 'post',
    params: parameter
  })
}

export function createFileRecord(parameter) {// 文件列表
  return axios({
    url: 'files/add_file',
    method: 'post',
    params: parameter
  })
}