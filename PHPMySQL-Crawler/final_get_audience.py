#!/usr/bin python3
# -*- coding:utf-8 -*-
# Author:XXG

import requests
import time
import json
import pymysql
from concurrent.futures import ThreadPoolExecutor
import threading
from multiprocessing import Lock
import signal
import time
import os
import sys
import random




SLEEP_TIME = 10


db_config = {
    'host': '1.1.1.1',
    'username': 'bilibili',
    'password': '********',
    'database': 'bilibili'
}




class DB():

    # 初始化数据库连接
    def __init__(self, config):

        # try:
        self.db = pymysql.connect(config['host'], config['username'], config['password'], config['database'], charset='utf8')
        self.cursor = self.db.cursor()
        try:
            pass
        except Exception as e:
            print(e)
            exit(0)

    def __del__(self):
        # self.db.close()
        pass

    # 插入数据, 接受参数 data = {'aid' = xxx, 'tid' = xxx, .....}
    def InsertData(self, data):

        try:

            sql = """INSERT INTO audience_statistics(all_count, web_online, play_online)
                        VALUES (%(all_count)s, %(web_online)s, %(play_online)s);
                        """
            self.cursor.execute(sql, data)      # 防止sql注入
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(e)

            return e.args[0]

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.bilibili.com',
        'Referer': 'https://www.bilibili.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }


# 获取数据，返回json，交给parse_data()
def get_intro():
    # url = "https://api.bilibili.com/x/web-interface/online?callback=jqueryCallback_bili_646486338944855&jsonp=jsonp&_=1553955125435"
    url = "https://api.bilibili.com/x/web-interface/online?jsonp=jsonp&_={}"

    ts = int(time.time() * 1000)

    req = requests.get(url.format(ts), timeout=4)

    if req.status_code == 200:
        data_json = req.json()
        if data_json['code'] == 0:
            return data_json
        else:
            return None
    else:
        print('[Error]\t%s' % req.status_code)
        print(req.text)
        return None


# 解析json中的字段，返回字典，准备存入db
def parse_data(intro_json):
    if intro_json:

        data = intro_json['data']
        dict = {
            'all_count': data['all_count'],
            'web_online': data['web_online'],
            'play_online': data['play_online']
        }
        return dict
    else:
        return None


def save_to_db(dict, db):
    if dict:
        error_code = db.InsertData(dict)
        if error_code:  # 主db、备份db同时写成功才返回true
            return True
    return False


def audience_watcher():
    db = DB(db_config)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    print("DB init!")

    count = 0
    while True:
        count += 1

        try:
            intro_json = get_intro()
            dict = parse_data(intro_json)
            error_code = save_to_db(dict, db)
            if error_code == True:
                pass
            else:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print('[ERROR]\tfail!')

            # 控制访问频率
            time.sleep(SLEEP_TIME)

        except Exception as e:
            print("[audience_watcher]")
            print('[Error]\t%s', e.args)




if __name__ == "__main__":
    audience_watcher()
