#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import html5lib
from pyecharts import  Bar

ALL_DATA = []

def craw_tmp(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode('utf-8')
    # feature:html.parser   html5lib 解析器
    soup = BeautifulSoup(text, 'html5lib')
    con_tab = soup.find('div', attrs={'class': 'conMidtab'})

    tables = con_tab.find_all('table')
    for tab in tables:
        trs = tab.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            if index == 0:
                city_td = tds[1]
            else:
                city_td = tds[0]
            cit = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({'city': cit, "temp":  int(min_temp)})


def main():
    urls = {

        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    }
    for url in urls:
        craw_tmp(url)

    # 分析数据   根据最低气温进行排序
    # def sort_key(data):
    #     min_tem = data['temp']
    #     return min_tem
    ALL_DATA.sort(key=lambda data: data['temp'])
    print(ALL_DATA)
    data = ALL_DATA[0:10]

    citys = list(map(lambda x: x['city'], data))
    temps = list(map(lambda x: x['temp'], data))
    chart = Bar('中国最低天气排行榜')
    chart.add('', citys, temps)
    chart.render('temperature.html')







# stripped_strings

if __name__ == '__main__':
    main()