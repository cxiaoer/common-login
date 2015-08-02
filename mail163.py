# coding:utf-8

import requests
import re
import json

if __name__ == '__main__':
    session = requests.Session()
    login_params = {
        'df': 'mail126_letter',
        'from': 'web',
        'funcid': 'loginone',
        'iframe': 1,
        'language': -1,
        'passtype': 1,
        'product': 'mail126',
        'verifycookie': -1,
        'net': 'failed',
        'race': '-2_-2_-2_db',
        'uid': 'chenwennothing@126.com',
        'hid': '10010102'
    }


    login_data = {
        'username': 'xxxxxxx',
        'savelogin': 0,
        'url2': 'http://mail.126.com/errorpage/error126.htm',
        'password': 'xxxxxxx'
    }
    first_res = session.post('https://mail.126.com/entry/cgi/ntesdoor', params=login_params,data=login_data)
    # print first_res.content
    second_url = re.search(r'href\s=\s"(.*?)"', first_res.content).group(1)
    print second_url
    sid = re.search(r'sid=(.*?)&', second_url).group(1)
    print sid
    second_res = session.get(second_url).content
    # print second_res
    search_params = {
        'sid': sid,
    }

    search_data = {
        'fid': 0,
        'start': 0,
        'limit': 100,
        'thread': 'false',
        'keyword': '账单',
        'searchType': 'FULL',
        'skipLockedFolders': 'true'
    }

    search_res = session.post('https://ssl.mail.126.com/jy6/xhr/list/search.do', params=search_params, data=search_data)
    print search_res.content
    # search_items = json.loads(search_res, encoding='gbk')
    # print search_items

    download_data = {
        'mid': '89:1tbiWRzCDVPI+WOXpgAAs6_142d:4775:h:q:g',
        'filterImages': 'false',
        'markRead': 'true'
    }

    download_res = session.post('https://ssl.mail.126.com/jy6/xhr/msg/read.do', params=search_params, data=download_data)
    print download_res.content