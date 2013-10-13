connect-python-sdk-oauth2-for-qq
================================

= 简介 =

PYTHON SDK基于QQ互联OAuth2.0协议的server-side模式， 封装了登录流程及调用类似获取用户信息所需的基础代码。


= 说明 =

开发者需按下面的说明修改代码，并按需要调用skd中提供的方法就可以在网站上实现“QQ登录”功能。

*1. 完成【QQ登录】准备工作

( [查看] http://wiki.opensns.qq.com/wiki/【QQ登录】开发攻略_Server-side#.E5.87.86.E5.A4.87.E5.B7.A5.E4.BD.9C )

*2. 使用前先修改 comm/qq_conf.py 中OauthVars类的4个变量:

        这4个变量需要自已配置，其中appid, appkey是腾讯提供的，callback是提交给腾讯许可的回调链接，scope是需要使用的openapi。
       
        self.Oauth_appid=''              # APP ID

        self.Oauth_appkey=''            # KEY

        self.Oauth_callback=''          # 回调地址

        self.Oauth_scope='get_user_info,'     # 请求用户授权时向用户显示的可进行授权的列表, 英文逗号分隔

*3. 在页面添加QQ登录按钮。详见文档说明:

（ [查看] http://wiki.opensns.qq.com/wiki/【QQ登录】开发攻略_Server-side#Step1.EF.BC.9A.E6.94.BE.E7.BD.AEQQ.E7.99.BB.E5.BD.95.E6.8C.89.E9.92.AE ）

*4.  编写流程代码。详见文档:
(
[http://wiki.opensns.qq.com/wiki/【QQ登录】文档资源 查看] http://wiki.opensns.qq.com/wiki/【QQ登录】文档资源 )


