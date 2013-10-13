# -*- coding: utf-8 -*-

"""
Oauth2.0 Client SDK 用于 QQ 登录及openapi调用。
"""
__author__ =  'Su Wei (objcc1@gmail.com)'
__version__=  '0.2'

from comm.qq_conf import OauthVars
try: import json 
except ImportError: import simplejson as json
import time, urllib, urllib2, logging

oauth_conf = OauthVars()

class OauthClient(object):
    """
    OAuth2.0 QQ登录及调用openapi所需类。
    """

    def __init__(cls, token=None, openid=None):
        """ 构造函数用于已成功登录过并且token没过期的用户 """
        object.__init__(cls)
        cls.token = token
        cls.openid = openid

        #初始化openapi_url
        if token is not None and openid is not None:
            cls.openapi_url = oauth_conf.Oauth_openapi_url.replace('<token>',cls.token).replace('<openid>',openid)
        else: 
            cls.openapi_url = None

    def gen_csrf(cls):
        """ 生成csrf串，用于防止重放攻击。"""
        return str(time.time())

    def get_authorize_url(cls, csrf=''):
        """ 生成登录链接，csrf参数需用户调用时传递，并在调用前保存(如session)，在回调函数中验证是否有效。"""
        return oauth_conf.Oauth_authorize_url.replace('<csrf>',csrf)

    def urlencode(cls, param={}):
        """ 
        返回url encoded query串，param是query串的dict结构，可使用query2dict将query串转为dict。
        """
        if param is None: return None
        return urllib.urlencode(param)

    def _http_fetch(cls, url, data=None, timeout=60):
        """ 返回http urlopen file handle """
        logging.error('urlopen: %s' % url)
        try:
            fd = urllib2.urlopen(url, data=data, timeout=timeout)
        except:
            logging.error('urlopen failed: %s' % url)
            return None
        return fd

    def query2dict(cls, query_str):
        """ 返回query_str串的dict结构 """
        query_dict={}
        try:
          splited = query_str.split('&')
          for kv in splited:
            k,v = kv.split('=')
            query_dict[k]=v
        except:
          return None
        return query_dict

    def request_token(cls, code=None, csrf=''):
        """ 获取token串，调用前确保code是从QQ OAuth2.0登录回调URL中获取到值。 """
        if code is None: return None
        token_url = oauth_conf.Oauth_token_url.replace('<csrf>',csrf).replace('<code>',code)
        fd = cls._http_fetch(token_url)
        if fd is None: return None

        try:
          content = fd.read()
          token_dict = cls.query2dict(content)
          if token_dict is None: return None
        except:
          logging.error("requst_token: %s" % content)
          return None

        cls.token = token_dict['access_token']

        return token_dict

    def request_openid(cls):
        """ 
        获取openid串，代表用户的唯一身份，调用前确保成功调用过request_token函数，即cls.token已正确设置。
        """
        if cls.token is None: return None
        openid_url = oauth_conf.Oauth_openid_url.replace('<token>',cls.token)
        fd = cls._http_fetch(openid_url)
        if fd is None: return None

        try:
          x = fd.read()
          if x.find('callback') > -1:
             pos_lb = x.find('{')
             pos_rb = x.find('}')
             x = x[pos_lb:pos_rb+1]
             openid_dict = json.loads(x,encoding='utf-8')
             openid = openid_dict['openid']
        except:
          logging.error("requst_openid: %s" % x)
          return None

        cls.openid = openid
        return openid

    def init_openapi_url(cls, token=None, openid=None):
        """
        初始化openapi_url，装载所有api调用必需传的参数，成功返回True，失败返回False。
        如不传参数，调用前确保成功调用过request_openid等方法。
        """

        if token is None and cls.token is None: return False

        if openid is not None: cls.openid = openid
        if token is not None: cls.token = token

        cls.openapi_url = oauth_conf.Oauth_openapi_url.replace('<token>',cls.token)

        if oauth_conf.Oauth_openapi_url.find('<openid>')>0: 
            if cls.openid is None: return False
            cls.openapi_url = cls.openapi_url.replace('<openid>',cls.openid)

        return True

    def request_openapi(cls, api_path_str, query_str='', post_str=None):
        """
        调用openapi，api_path_str是openapi中提供的调用链接中的url_path部分，因为domain都是相同的https://graph.qq.com
        如获取登录用户信息的URL是：https://graph.qq.com/user/get_user_info，
        这里的对应的api_path_str只需传递user/get_user_info即可。
        调用成功返回dict对象。
        调用前确保成功调用过init_openapi_url方法。
        即cls.token, cls.openid已正确设置, cls.openapi_url已初始化。
        """

        if api_path_str is None: return None
        openapi_url = cls.openapi_url.replace('<api>',api_path_str).replace('<query_str>',query_str)
        fd = cls._http_fetch(openapi_url, post_str)
        if fd is None: return None

        try:
          x = fd.read()
          res_dict = json.loads(x,encoding='utf-8')
        except:
          logging.error("requst_openapi: %s, %s" % (api_path_str,x))
          return None

        return res_dict
