#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# pip list 显示当前安装的库

import requests
from bs4 import BeautifulSoup
import json
import time
import pai_parser
import urllib3
import threading
# sudo pip install

BASE_RUL = "https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false"
DETAIL_URL = 'https://www.lagou.com/jobs/4317425.html'
PAGE_LIST = []
# 详情
def crew_detail(id):
    url = 'https://www.lagou.com/jobs/%s.html' % id
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
        'Host': 'www.lagou.com',
        'Upgrade-Insecure-Requests': '1',


    }
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.content, features='html.parser')
    job_bt = soup.find('dd', attrs={'class': 'job_bt'})

    print(job_bt.text)


def main():

    positions = []
    for i in range(1, 10):
        data = {
            'first': 'true',
            'kd': 'python',
            'pn': i
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/jobs/list_python&px=efault&city=%E5%8C%97%E4%BA%AC',
            'X-Anit-Forge-Code': '0',
            'X-Anit-Forge-Token': 'None',
            'X-Requested-With': 'XMLHttpRequest'

        }
        try:
            result = requests.post(BASE_RUL, headers=headers, data=data)
            # ajax请求
            # post data
            json_result = result.json()
            print(json_result)
            composition = json_result['content']['positionResult']['result']
            positions.extend(composition)
            time.sleep(5)
        except IOError:
            continue

        line = json.dumps(positions, ensure_ascii=False)
        with open('lagouMessage.json', 'w') as fp:
            fp.write(line)


if __name__ == '__main__':
     # main()
     crew_detail('4317425')
