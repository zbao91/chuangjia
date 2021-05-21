# 007app3

007app 新版本

apps
    BaseHandler
    
    设置yc_id/uid 实例属性
    设置device 实例属性
    
    - 1 获取参数

       自定义了get_int/str_argument 获取整数/字符串参数，为定义default表示必填，会raise MissArg异常

    自动记录log日志->redis->mogodb
        operat  类属性 or url定义的name

    overwrite application 的log_request
    overwrite handler 的 write_error 和send_error 方法，都自定义异常进行捕获处理

关于异常

    异常中设置return_code 和 return_msg, 作为返回的code值 和msg

    post/get 中直接raise core.errors 的 子类异常

    由handler 的 write_error 和send_error 处理



关于权限

```
   权限在handler prepare中处理，不同的handler子类定义自己的权限列表
   
   模块 middleware.valid 进行权限判断（权限类型)
   
```


BaseERPHandler 说明

```
类变量
- args 可为dict或者可迭代对象
    - 字典时{参数名：参数默认值)
    - 可迭代对象 [(参数名, 默认值， 是否必填)]  默认值和是否必填可以省略（认为空字符串和False）
- arg_rename = {参数重命名}
   {old_name: new_name}
- role 权限
- login  bool是否需要登录
- uri rpc服务的地址

- callback
   rpc返回时，得到返回body的字典对象
   可以覆写 is_expected_result 来对result对象进行处理



- method
  GET/POST
```


静态文件

```python

- app下载页
/static/app_download.html

- 零件分享页
/static/partshare/in/index.html 成功
/static/partshare/out/index.html 失败

- h5 套餐页
/static/h5/index.html
```
