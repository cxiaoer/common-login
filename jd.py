# coding:utf-8

"""
京东模拟登陆
"""
import requests
from bs4 import BeautifulSoup
import time

session =requests.Session()
header = {
    'user_agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
}
class Jd(object):
    """京东的用户名和密码"""
    def __init__(self, username, password):
        super(Jd, self).__init__()
        self.username = username
        self.password = password

    def login(self):
        soup = BeautifulSoup(session.get('https://passport.jd.com/new/login.aspx', verify=False, headers=header).content)
        uuid = soup.find(id='uuid')['value']
        input = soup.find_all(type='hidden')[4]
        print uuid
        print input['name']
        print input['value']

        data = {
            'uuid': uuid,
            'loginname': self.username,
            'nloginpwd': self.password,
            'loginpwd': self.password,
            'machineNet': '',
            'machineCpu': '',
            'machineDisk': '',
            'authcode': '',
            input['name']: input['value']
        }

        params = {
            'uuid': uuid,
            'ReturnUrl': 'http://www.jd.com/?utm_source=jd.com',
            'r': '0.05012108405860494'
        }

        res = session.post('https://passport.jd.com/uc/loginService', params=params, data=data, headers=header, verify=False)
        print res.url
        print res.content

if __name__ == '__main__':
    jd = Jd('xxxxxx', 'xxxxxx')
    jd.login()