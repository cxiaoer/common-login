# coding:utf-8

import requests

import re

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
    }
    data = {
        'accountType': '02',
        'appId': '8013411507',
        'returnUrl': 'http://hermesw034.mail.21cn.com/webmail/uniPlatformLoginReturn.do?',
        'userName': 'xxxxxxx',
        'mail': '@189.cn',
        'password': 'xxxxxxx',
        'ValidateCode': ''
    }

    session = requests.Session()
    first_res = session.post('https://open.e.189.cn/api/common/loginSubmit.do', data=data,
                             allow_redirects=False).content
    # print first_res.headers
    second_url = re.search(r'href="(.*)"', first_res).group(1)
    # print second_url
    second_res = session.get(second_url, allow_redirects=False).content
    # print second_res
    three_url = re.search(r'"toUrl":"(.*)"', second_res).group(1)
    print three_url
    three_res = session.get(three_url, allow_redirects=False)

    final_res = session.get('http://hermesw034.mail.21cn.com/webmail/signOn.do').content
    print final_res
