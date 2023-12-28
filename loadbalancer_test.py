#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import re
import urllib.request
import threading
import argparse
import matplotlib.pyplot as plt


# 定义一个函数，输入网址，返回该网页上的IP地址
def get_ip_address(url):
    # 打开网页
    response = urllib.request.urlopen(url)
    # 读取网页内容
    html = response.read().decode('utf-8')
    # 使用正则表达式匹配IP地址
    pattern = re.compile('\d+\.\d+\.\d+\.\d+')
    ip_address = pattern.search(html)
    # 返回IP地址
    return ip_address.group()


# 定义一个函数，输入网址和访问次数，输出该网页上的IP地址和出现次数
def get_ip_address_count(url, count, result_dict):
    # 定义一个列表，用于存储所有IP地址
    ip_list = []
    # 循环访问网页
    for i in range(count):
        # 调用函数，获取IP地址
        ip_address = get_ip_address(url)
        # 将IP地址添加到列表中
        ip_list.append(ip_address)
    # 统计每个IP地址出现的次数
    for ip in ip_list:
        if ip in result_dict:
            result_dict[ip] += 1
        else:
            result_dict[ip] = 1

    # 用图表的形式展示每个IP地址的出现次数
    for x, y in zip(result_dict.keys(), result_dict.values()):
        plt.text(x, y + 0.05, '%d' % y, ha='center', va='bottom')
    plt.bar(result_dict.keys(), result_dict.values())
    plt.show()


# 定义一个函数，输入网址和访问次数，输出该网页上的IP地址和出现次数
def get_ip_address_count_thread(url, count, result_dict):
    # 定义一个列表，用于存储所有线程
    threads = []
    # 循环创建线程
    for i in range(count):
        # 创建线程，调用函数，获取IP地址
        t = threading.Thread(target=get_ip_address, args=(url,))
        # 将线程添加到列表中
        threads.append(t)
    # 循环启动线程
    for t in threads:
        t.start()
    # 循环等待线程结束
    for t in threads:
        t.join()

    # 在所有线程结束后，调用函数，输出该网页上的IP地址和出现次数，使用单线程方式
    get_ip_address_count(url, count, result_dict)


if __name__ == '__main__':
    # 创建解析器对象
    parser = argparse.ArgumentParser(description='Get IP address and count of a website')

    # 添加参数
    parser.add_argument('url', type=str, help='the URL of the website')
    parser.add_argument('count', type=int, help='the number of times to access the website')

    # 解析参数
    args = parser.parse_args()

    # 调用函数，输入网址和访问次数，输出该网页上的IP地址和出现次数，使用多线程方式
    get_ip_address_count_thread(args.url, args.count, {})
