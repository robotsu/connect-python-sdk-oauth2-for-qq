# -*- coding: utf-8 -*-

"""
OAuth2登录所需基本变量
"""
class OauthVars:
    def __init__(self):

        """
        这4个变量需要自已配置，其中appid, appkey是腾讯提供的，callback是提交给腾讯许可的回调链接，scope是需要使用的openapi。
        """
        self.Oauth_appid=''					# APP ID
        self.Oauth_appkey=''		                        # KEY
        self.Oauth_callback=''	                                # 回调地址
        self.Oauth_scope='get_user_info,'            		# 请求用户授权时向用户显示的可进行授权的列表, 英文逗号分隔


        """
        下面这些变量不用修改，是auth2.0登录QQ及调用openapi必用的链接，如果不清楚请保持不变。
        """
        # oauth2.0 url prefix
        self.Oauth_2_url_prefix='https://graph.qq.com/oauth2.0'

        # authorize_url
        self.Oauth_authorize_url='%s/authorize?response_type=code&client_id=%s&redirect_uri=%s&scope=%s&state=<csrf>' % \
            (self.Oauth_2_url_prefix, self.Oauth_appid, self.Oauth_callback, self.Oauth_scope)

        # token_url
        self.Oauth_token_url='%s/token?grant_type=authorization_code&client_id=%s&client_secret=%s&code=<code>&state=<csrf>&redirect_uri=%s' % \
            (self.Oauth_2_url_prefix, self.Oauth_appid, self.Oauth_appkey, self.Oauth_callback)

        # openid_url
        self.Oauth_openid_url='%s/me?access_token=<token>' % self.Oauth_2_url_prefix

        # openapi_url
        self.Oauth_openapi_url='https://graph.qq.com/<api>?access_token=<token>&oauth_consumer_key=%s&openid=<openid>&format=json&<query_str>' % self.Oauth_appid

