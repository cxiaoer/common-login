# coding:utf-8
import requests

from bs4 import BeautifulSoup
import os
import socket


"""
知乎的登陆关键是访问首页时，通过页面拿到登陆时要用的_xsrf参数
"""
login_url = 'http://www.zhihu.com/login'
zhihu_index = 'http://www.zhihu.com'
header_info = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
    'Host': 'www.zhihu.com',
    'Origin': 'http://www.zhihu.com',
    'Connection': 'keep-alive',
    'Referer': 'http://www.zhihu.com',
    'Content-Type': 'application/x-www-form-urlencoded',
}

session = requests.session()
data = {
    'email': 'xxxxxx',
    'password': 'xxxxxx',
    'rememberme': 'y'
}
data['_xsrf'] = BeautifulSoup(session.get(zhihu_index).content).find(type='hidden')['value']
print data
html = session.post(login_url, data, headers=header_info)
# print html.content

# get img source url
def getImgSrc(html):
    for item in BeautifulSoup(html.content).find_all('img', class_='js-captcha-img'):
        img_src = item['src']
        if None != img_src:
            print '验证码的请求地址为:\n' + zhihu_index + img_src
            return zhihu_index + img_src
        else:
            return None


# download the img to local
def downloadImg(img_src):
    r = session.get(img_src, stream=True, headers=header_info)
    fileName = img_src.split('=')[-1]
    print fileName

    if os.path.exists('img'):
        print 'img目录已经存在!'
    else:
        os.mkdir('img')
    with open(os.getcwd() + '\img' + '\\' + fileName + '.gif', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            # filter out keep-alive new chunks
            if chunk:
                f.write(chunk)
                f.flush()


# get the the input from the console
def getValidCode():
    valid_code = raw_input("请输入验证码:\n")
    return valid_code


img_src = getImgSrc(html)
if None != img_src:
    downloadImg(img_src)
    data['captcha'] = getValidCode()
    print data
    after_html = session.post(login_url, data, headers=header_info)
    with open(os.getcwd() + '\zhihu.html', 'wb') as f:
        f.write(after_html.content)
        # print after_html.content
else:
    print html.content


# search some content in zhihu
def search(title):
    _search_url = 'http://www.zhihu.com/search'
    params = {'q': title, 'type': 'question'}
    _search_result = session.get(_search_url, params=params)
    # print _search_result.url
    # with open(os.getcwd() + '\search.html', 'wb') as f:
    #     f.write(_search_result.content)
    # print _search_result.content

    #get the title
    for item in BeautifulSoup(_search_result.content).find_all('a', class_='question-link'):
        print item


search('爬虫')









