from __future__ import division
# coding:utf-8


import requests
import re
import time
import base64
import json
import shutil
import os
import sys

"""
yunpan login
visit the index --------> get the [BAIDUID] ---------> visit the get token api-------------> get the [token]

------> user the [token] to visit the login api -----------> get the key cookie param [BDUSS] ----- > use the cookie to visit the home ----> success!

in fact, there are only two cookie item matters, i have tried , the [BAIDUID] and [BDUSS]



"""

INDEX_URL = 'http://pan.baidu.com/'
LOGIN_URL = 'https://passport.baidu.com/v2/api/?login'
HOME_URL = 'http://pan.baidu.com/disk/home'

session = requests.Session()
token_pattern = re.compile(r'"token"\s:\s"(.*?)"')
bdstoken_pattern = re.compile(r'yunData.MYBDSTOKEN\s=\s"(.*?)";')


class YunDisk(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.__token = None
        self.__bdstoken = None

    def __visit_index(self):
        session.get(INDEX_URL)

    def __get_token(self):
        base_params = {
            'tpl': 'netdisk',
            'apiver': 'v3',
            'class': 'login',
            'logintype': 'basicLogin',
            'callback': 'bd__cbs__ih2k0y'
        }
        key_params = {'tt': int(time.time() * 1000)}
        params = dict(key_params, **base_params)
        # res = session.get('https://passport.baidu.com/v2/api/?getapi', params=params, verify=False)
        res = session.get('https://passport.baidu.com/v2/api/?getapi', params=params)
        content = res.content
        if content is not None:
            print 'Get the token success!'
            match = token_pattern.search(content.replace('\'', '"'))
            if match is not None:
                self.__token = match.group(1)
                print 'token=%s' % self.__token

    def __get_sign(self):
        res = session.get(HOME_URL).content
        sign1 = re.search(r'yunData.sign1\s=\s\'(.*?)\';', res).group(1)
        sign3 = re.search(r'yunData.sign3\s=\s\'(.*?)\';', res).group(1)
        timestamp = re.search(r'timestamp = \'(.+?)\';', res).group(1)

        def sign2(j, r):
            a = []
            p = []
            o = ''
            v = len(j)
            for q in xrange(256):
                a.append(ord(j[(q % v)]))
                p.append(q)

            u = 0
            for q in xrange(256):
                u = (u + p[q] + a[q]) % 256
                p[q], p[u] = p[u], p[q]

            i = 0
            u = 0
            for q in xrange(len(r)):
                i = (i + 1) % 256
                u = (u + p[i]) % 256
                p[i], p[u] = p[u], p[i]
                k = p[((p[i] + p[u]) % 256)]
                o += chr(ord(r[q]) ^ k)
            return base64.b64encode(o)

        self.key_params = {'sign': sign2(sign3, sign1), 'timestamp': timestamp}

    def __pre_login(self):
        base_params = {
            'staticpage': 'http://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html',
            'charset': 'utf-8',
            'tpl': 'netdisk',
            'subpro': '',
            'apiver': 'v3',
            'codestring': '',
            'safeflg': '0',
            'u': 'http://pan.baidu.com/',
            'isPhone': 'false',
            'quick_user': '0',
            'logintype': 'basicLogin',
            'logLoginType': 'pc_loginBasic',
            'idc': '',
            'loginmerge': 'true',
            'verifycode': '',
            'mem_pass': 'on',
            'ppui_logintime': '',
            'callback': 'parent.bd__pcbs__f4bmqo'
        }
        key_params = {}
        self.__visit_index()
        self.__get_token()

        now = int(time.time() * 1000)
        key_params['tt'] = str(now)
        key_params['username'] = self.username
        key_params['password'] = self.password
        key_params['token'] = self.__token
        data = dict(key_params, **base_params)
        session.post(LOGIN_URL, data=data)

    def login(self):
        self.__pre_login()
        home_res = session.get(HOME_URL)
        res_content = home_res.content
        if res_content is not None:
            print 'Login success!'
            match = bdstoken_pattern.search(res_content)
            if match is not None:
                self.__bdstoken = match.group(1)
                print 'sessionId=%s' % self.__bdstoken

    def search(self, keyword):
        base_params = {
            'channel': 'chunlei',
            'clienttype': '0',
            'web': '1',
            'app_id': '250528',
            'num': 100,
            'page': 1,
            'dir': '',
            'order': 'time',
            'desc': 1,
            'showempty': 0,
            'searchPath': 'null',
            'recursion': 1,
        }

        key_params = {'_': self.__bdstoken, 'key': keyword}
        params = dict(key_params, **base_params)
        search_res = session.get('http://pan.baidu.com/api/search', params=params)
        print search_res.content

    def download(self, fid):
        base_params = {
            'type': 'dlink',
            'bdstoken': self.__bdstoken,
            'channel': 'chunlei',
            'clienttype': '0',
            'web': '1',
            'app_id': '250528'
        }
        if not hasattr(self, 'key_params'):
            self.__get_sign()
        key_params = self.key_params
        key_params['fidlist'] = '[' + str(fid) + ']'
        params = dict(key_params, **base_params)
        download_res = session.get('http://pan.baidu.com/api/download', params=params).content
        obj = json.loads(download_res)
        for item in obj['dlink']:
            print item['dlink']
            content = session.get(item['dlink'], stream=True)
            # print conten.content
            print content.status_code
            res_headers = content.headers
            file_name = re.search(r'"(.*?)"', content.headers['content-disposition']).group(1)
            file_size = content.headers['content-length']
            print file_name
            print file_size
            print res_headers
            if content.status_code == 200:
                path = os.getcwd() + '/' + file_name
                if os.path.exists(path):
                    print file_name + ' is exists!'
                    os.remove(path)
                print 'start downloading-----------------------!'
                with open(file_name, 'wb') as f:
                    i = 0
                    for item in content.iter_content(chunk_size=1024):
                        f.write(item)
                        # print '%.2f' % (i / (int(file_size) / 1024))
                        i += 1
                        if i % 20 == 0:
                            sys.stdout.write('#' + '\b\b')
                            sys.stdout.flush()
                print '\n'
                # print i
                print 'download success------------------------!'

                # if content.status_code == 200:
                #     with open('python.pdf', 'wb') as f:
                #         shutil.copyfileobj(content.raw, f)


def share_download(url):
    session = requests.Session()
    base_params = {
        'bdstoken': '',
        'channel': 'chunlei',
        'clienttype': '0',
        'web': '1',
        'app_id': '250528'
    }
    key_params = {}
    html = session.get(url).content
    sign = re.search(r'yunData.SIGN\s=\s"(.*?)";', html).group(1)
    timestamp = re.search(r'yunData.TIMESTAMP\s=\s"(.*?)"', html).group(1)
    share_uk = re.search(r'yunData.SHARE_UK\s=\s"(.*?)"', html).group(1)
    share_id = re.search(r'yunData.SHARE_ID\s=\s"(.*?)"', html).group(1)
    file_list = re.search(r'yunData.FILEINFO\s=.*\[(.*})\];', html).group(1)
    print file_list

    # files = json.loads('['+file_list+']')
    file_id = raw_input('Which file do you want to download? please input the file id!\n')

    # construct the query params
    key_params['sign'] = sign
    key_params['timestamp'] = timestamp
    params = dict(key_params, **base_params)
    # construct the post data
    data = {
        'encrypt': 0,
        'product': 'share',
        'uk': share_uk,
        'primaryid': share_id,
        'fid_list': '[' + file_id + ']'
    }
    download_res = session.post('http://pan.baidu.com/api/sharedownload', params=params, data=data)
    print download_res.content


if __name__ == '__main__':
    # username = raw_input("please input username:\n")
    # password = raw_input("please input password:\n")

    username = 'xxxxxx'
    password = 'xxxxxx'
    yundisk = YunDisk(username, password)
    yundisk.login()
    # yundisk.search('python')
    yundisk.download(495708917252431)
    # share_download('http://pan.baidu.com/s/1dDlELjz')
