#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re
import threading
import urllib.request
import matplotlib.pyplot as plt

REAL_IP_LIST = []  # 用于存放获取到的Real_IP的列表
LOCK = threading.Lock()  # 线程锁实例化


def get_url(ip):
    """
    根据给定的VIP地址发起访问请求，获取页面上的信息，提取Real_IP
    :param ip: VIP地址
    :return: None
    """
    with urllib.request.urlopen(f'http://{ip}') as response:
        html = response.read().decode('utf-8')
    match_ip = re.compile(r'\d+\.\d+\.\d+\.\d+')  # 匹配Real_IP的正则表达式
    get_ip = match_ip.search(html)  # 获取网页中的匹配正则表达式的结果
    with LOCK:  # 将获取到的Real_IP追加到列表中
        REAL_IP_LIST.append(get_ip.group())


if __name__ == '__main__':
    vip = input(f'请输入需要测试的VIP地址：')
    count = input(f'请输入需要发起测试的访问量：')
    threading_list = []  # 线程列表
    result_dict = {}  # 统计字典

    for i in range(int(count)):
        pre_get = threading.Thread(target=get_url, args=(vip,))  # 创建线程，执行get_url函数，参数为VIP地址
        threading_list.append(pre_get)  # 将线程添加到线程列表中
        pre_get.start()  # 启动线程

    for thread in threading_list:  # 等待所有线程执行完毕
        thread.join()

    # 统计列表内出现的每一个元素的次数，形成一个字典
    for real_ip in REAL_IP_LIST:
        result_dict[real_ip] = result_dict.get(real_ip, 0) + 1  # 如果字典中不存在这个元素，则初始为0，再+1；如果存在则直接+1

    # 绘制柱状图
    for x, y in zip(result_dict.keys(), result_dict.values()):
        plt.text(x, y + 1, '%d' % y, ha='center', va='bottom')  # 绘制柱状图上的数字
    plt.bar(result_dict.keys(), result_dict.values())  # 绘制柱状图
    plt.show()  # 显示柱状图
