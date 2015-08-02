# coding:utf-8
"""
1 use wap login is more easier
2 when we login success, we can do anything we want

"""
import requests
import json

WAP_LOGIN_URL = 'https://passport.weibo.cn/signin/login?entry=mweibo' \
                '&res=wel&wm=5091_0026' \
                '&r=http%3A%2F%2Fm.weibo.cn%2F%3Fwm%3D5091_0026'
LOGIN_API = 'https://passport.weibo.cn/sso/login'
FEED_URL = 'http://m.weibo.cn/index/feed?format=cards'

header_info = {
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    # what the fuck, if don't the params as follows, the request forbidden
    'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=5091_0026&r=http%3A%2F%2Fm.weibo.cn%2F%3Fwm%3D5091_0026',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

login_params = {
    'savestate': '1',
    'ec': '1',
    'pagerefer': '',
    'entry': 'mweibo',
    'loginfrom': '',
    'client_id': '',
    'code': '',
    'hff': '',
    'hfp': ''
}

session = requests.session()


class Weibo(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        res = session.get(WAP_LOGIN_URL)
        login_params['username'] = self.username
        login_params['password'] = self.password
        login_res = session.post(LOGIN_API, data=login_params, headers=header_info)
        if login_res:
            real_res = login_res.content
            # print real_res
            data = json.loads(real_res, encoding='gbk')
            print data['data']['crossdomainlist']

    def get_feed(self):
        self.login()
        feed_res = session.get(FEED_URL)
        json_res = feed_res.content
        if json:
            data = json.loads(json_res, encoding='gbk')
            print data



if __name__ == '__main__':
    # username = raw_input("请输入你的微博用户名:\n")
    # password = raw_input("请输入你的微博密码:\n")
    username = 'xxxxxx'
    password = 'xxxxxx'
    weibo = Weibo(username, password)
    # weibo.login()
    weibo.get_feed()