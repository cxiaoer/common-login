# coding:utf-8
"""
51job爬虫
"""
import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
}
class ZhiLian(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        index_soup = BeautifulSoup(session.get('http://my.51job.com/my/My_SignIn.php', headers=header).content)
        middle_url = index_soup.find(id='signin')['action']
        print middle_url
        data = {
            'username': self.username,
            'userpwd': self.password,
            'login_verify': '',
            'autologin': 0,
            'url': '',
            'x': 22,
            'y': 12
        }
        #包含自动重定向结果
        middle_res_content = session.post(middle_url, data=data, headers=header).content
        home = open('home_zhilian.html', 'wb')
        home.write(middle_res_content)

    #默认搜索杭州的
    def search(self, keyword):
        data = {
            'keywordtype': 2,
            'stype': 2,
            'jobarea': '080200',
            'keyword': keyword
        }
        search_res = session.post('http://search.51job.com/jobsearch/search.html?fromJs=1&lang=c', data=data, headers=header).content
        # print search_res
        # search_file = open('search_res.html', 'wb')
        # search_file.write(search_res)
        search_soup = BeautifulSoup(search_res)
        print search_soup.find(id='resultList')


if __name__ == '__main__':
    zhilian = ZhiLian('xxxxxx', 'xxxxxx')
    zhilian.login()
    zhilian.search('java')
