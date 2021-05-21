/* eslint-disable */
import Vue from 'vue'
export function timeFix() {
  const time = new Date()
  const hour = time.getHours()
  return hour < 9 ? '早上好' : hour <= 11 ? '上午好' : hour <= 13 ? '中午好' : hour < 20 ? '下午好' : '晚上好'
}

export function welcome() {
  const arr = ['休息一会儿吧', '准备吃什么呢?', '要不要打一把 DOTA', '我猜你可能累了']
  const index = Math.floor(Math.random() * arr.length)
  return arr[index]
}

/**
 * 触发 window.resize
 */
export function triggerWindowResizeEvent() {
  const event = document.createEvent('HTMLEvents')
  event.initEvent('resize', true, true)
  event.eventType = 'message'
  window.dispatchEvent(event)
}

export function handleScrollHeader(callback) {
  let timer = 0

  let beforeScrollTop = window.pageYOffset
  callback = callback || function () {
  }
  window.addEventListener(
    'scroll',
    event => {
      clearTimeout(timer)
      timer = setTimeout(() => {
        let direction = 'up'
        const afterScrollTop = window.pageYOffset
        const delta = afterScrollTop - beforeScrollTop
        if (delta === 0) {
          return false
        }
        direction = delta > 0 ? 'down' : 'up'
        callback(direction)
        beforeScrollTop = afterScrollTop
      }, 50)
    },
    false
  )
}

/**
 * Remove loading animate
 * @param value parent element value or class
 * @param timeout
 */
export function removeLoadingAnimate(value = '', timeout = 1500) {
  if (value === '') {
    return
  }
  setTimeout(() => {
    document.body.removeChild(document.getElementById(value))
  }, timeout)
}

export function uuid () {
  var s = []
  var hexDigits = "0123456789abcdef"
  for (var i = 0; i < 36; i++) {
    s[i] = hexDigits.substr(Math.floor(Math.random() * 0x10), 1)
  }
  s[14] = "4" // bits 12-15 of the time_hi_and_version field to 0010
  s[19] = hexDigits.substr((s[19] & 0x3) | 0x8, 1) // bits 6-7 of the clock_seq_hi_and_reserved to 01
  s[8] = s[13] = s[18] = s[23] = "-"
  var uuid = s.join("")
  return uuid
}

export function format (date, fmt) {
  if (/(y+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
  }
  let o = {
    'M+': date.getMonth() + 1,
    'd+': date.getDate(),
    'h+': date.getHours(),
    'm+': date.getMinutes(),
    's+': date.getSeconds()
  }
  for (let k in o) {
    let str = o[k] + ''
    if (new RegExp(`(${k})`).test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? str : padLeftZero(str))
    }
  }
  return fmt
}

export function checkPass(s){

  const mmCheck=/^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[~@#$%_!\*-\+=:,.\\?\[\]\{}]).{8,}$/ 
  const isbh=/.*[Ww][Aa][Ss][Uu].*/
  if(s.length < 8){
    return 0;
  }
  //var ls = 0;
  // if(s.match(/([a-z])+/)){
  //   ls++;
  // }
  // if(s.match(/([0-9])+/)){
  //   ls++;
  // }
  // if(s.match(/([A-Z])+/)){
  //   ls++;
  // }
  // if(s.match(/[^a-zA-Z0-9]+/)){
  //   ls++;
  // }
  if(!mmCheck.test(s)){
    return 1
  }
  if(isbh.test(s)){
    return 2
  }
  //return ls
}
    //时间校验 定时发布的计划下线时间不得早于发布时间
    export function  checkTime(publishDate,expireDate){ //定时发布的计划下线时间不得早于发布时间!
      var publishDatet = new Date(Date.parse(publishDate));//发布时间
      var expireDatet = new Date(Date.parse(expireDate));//计划下线时间
      if(expireDatet <= publishDatet){
        return {iskey:false,msg:'定时发布的计划下线时间不得早于发布时间!'}
      }else{
        return {iskey:true}
      }
    }
    export function  checkCurrTime(publishDate){ //发布时间不能小于当前时间
      var publishDatet = new Date(Date.parse(publishDate));//发布时间
      var currtime = new Date();//当前时间
      if(currtime > publishDatet){
        return {iskey:false,msg:'发布时间不能小于当前时间!'}
      }else{
        return {iskey:true}
      }
    }
    export function  checkExTime(expireDate){ //计划下线时间不能小于当前时间
      var expireDatet = new Date(Date.parse(expireDate));//下线时间
      var currtime = new Date();//当前时间
      if(currtime > expireDatet){
       return {iskey:false,msg:'计划下线时间不能小于当前时间!'}
      }else{
        return {iskey:true}
      }
    }
    /*
      ** randomWord 产生任意长度随机字母数字组合
      ** randomFlag-是否任意长度 min-任意长度最小位[固定位数] max-任意长度最大位
      ** xuanfeng 2014-08-28
      生成43位随机串：randomWord(43,,mima)
      */
    export function  randomWord(min,pwd){ 
        var str = "";
        var range = min;
        var arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        // 随机产生
        for(var i=0; i<range; i++){
          var pos = Math.round(Math.random() * (arr.length-1));
          str += arr[pos];
        }
        let base64=btoa(pwd)
        return `${str}${base64}`;
    }

    export function getHeaderOrganize3(){
        parent = null
        node = null
        let curOrganizeName = ''
        let organizes = Vue.ls.get('organizes')
        let organizeType = Vue.ls.get('organizeType')
        let organizeId = Vue.ls.get('organizeId')
        if(organizeType == '3'){ //区级直接返回
          curOrganizeName = Vue.ls.get('organizeName')
        }else if(organizeType == '4'){
          let temp = getParentId(organizes,organizeId)
          if(temp){
            let result = getNode(organizes,temp.parentId)
            curOrganizeName = result.title
          }
        }else if(organizeType == '5'){
          let temp1 = null
          temp1 = getParentId(organizes,organizeId)
          if(temp1){
            node = null
            let temp2 = getNode(organizes,temp1.parentId)
            if(temp2){
              node = null
              let result = getNode(organizes,temp2.parentId)
              if(result){curOrganizeName = result.title}
            }
          }
        }else{
          curOrganizeName = Vue.ls.get('organizeName')
        }
        return curOrganizeName
    }

    var parent = null
    export function getParentId(json, nodeId) { //根据value找到parentId
      for (var i = 0; i < json.length; i++) {
          if (parent) {
              break;
          }
          var obj = json[i];
          if (!obj || !obj.value) {
              continue;
          }
          if (obj.value == nodeId) {
              parent = obj
              break;
          } else {
              if (obj.children.length>0) {
                  getParentId(obj.children, nodeId)
              } else {
                  continue;
              }
          }
      }
      return parent;
  }

    var node = null
    export function getNode(json, nodeId) { //根据parentId 找到对应node
      for (var i = 0; i < json.length; i++) {
          if (node) {
              break;
          }
          var obj = json[i];
          if (!obj || !obj.value) {
              continue;
          }
          if (obj.id == nodeId) {
              node = obj
              break;
          } else {
              if (obj.children.length>0) {
                getNode(obj.children, nodeId)
              } else {
                  continue;
              }
          }
      }
      return node;
  }




