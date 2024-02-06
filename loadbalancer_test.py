#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import threading
import urllib.request
import matplotlib.pyplot as plt
import requests

REAL_IP_LIST = []
LOCK = threading.Lock()  # 线程锁实例化


def get_url(ip):
    with urllib.request.urlopen(f'http://{ip}') as response:
        html = response.read().decode('utf-8')
    get_ip = re.compile(r'\d+\.\d+\.\d+\.\d+')
    real_ip = get_ip.search(html)
    with LOCK:
        REAL_IP_LIST.append(real_ip)
    # return real_ip.group()
    # x = requests.get(f'http://{ip}')
    # return x.content.decode('utf-8')


if __name__ == '__main__':
    vip = input(f'请输入需要测试的VIP地址：')
    count = input(f'请输入需要发起测试的访问量：')
    threading_list = []
    result_dict = {}

    for i in range(int(count)):
        pre_get = threading.Thread(target=get_url, args=(vip,))
        threading_list.append(pre_get)
        pre_get.start()
        # with LOCK:
        #     REAL_IP_LIST.append(get_url(vip))

    for ii in threading_list:
        ii.join()

    print(REAL_IP_LIST)
    for real_ip in REAL_IP_LIST:
        result_dict[real_ip] = result_dict.get(real_ip, 0) + 1

    print(result_dict)

    for x, y in zip(result_dict.keys(), result_dict.values()):
        plt.text(x, y + 1, '%d' % y, ha='center', va='bottom')
    plt.bar(result_dict.keys(), result_dict.values())
    plt.show()
