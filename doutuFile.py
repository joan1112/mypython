#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import request
from bs4 import  BeautifulSoup
import urllib.request
import os
import pai_parser
import re
import html.parser as h
import threading
import time


BASE_URL = "http://www.doutula.com/photo/list/?page="
PAGE_URL = []
FACE_URL = []
glock = threading.Lock()
for x in range(1, 10):
    url = BASE_URL+str(x)
    PAGE_URL.append(url)


def download_image(page_url):
    splist = page_url.split('/')
    filename = splist.pop()
    print(filename, page_url)
    path = os.path.join('images', filename)
    urllib.request.urlretrieve(page_url, filename=path)


def producer():
    while True:
        glock.acquire()
        if len(PAGE_URL) == 0:
            glock.release()
            break
        else:
            page_url = PAGE_URL.pop()
            glock.release()
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
                req = urllib.request.Request(url=page_url, headers=headers)
                response = urllib.request.urlopen(req)
                content = response.read().decode('utf-8')
                soup = BeautifulSoup(content, features="html.parser")
                img_list = soup.find_all('img', attrs={'class': 'img-responsive lazy image_dta'})
            except IOError:
                continue
                print("Error: 没有找到文件或读取文件失败")
            else:
                print("内容写入文件成功")
                glock.acquire()
                for img in img_list:
                    src = img['data-original']
                    if src.startswith('http'):
                        url1 = img['data-original']
                    else:
                        url1 = 'https:' + src
                    FACE_URL.append(url1)
                    print(FACE_URL)
                glock.release()


def customer():
    while True:
        glock.acquire()
        if len(FACE_URL) == 0:
            glock.release()
            continue
        else:
            face_url = FACE_URL.pop()
            print("88888888" + face_url)
            glock.release()
            splist = face_url.split('/')
            filename = splist.pop()
            print(filename, face_url)
            path = os.path.join('images', filename)
            urllib.request.urlretrieve(face_url, filename=path)


def main():
    for b in range(3):
        th = threading.Thread(target=producer)
        th.start()

    for b in range(5):
        print(44444)
        th = threading.Thread(target=customer)
        th.start()


if __name__ == "__main__":
    main()


