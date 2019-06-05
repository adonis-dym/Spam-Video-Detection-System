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
import traceback


def set_timeout(num, callback):
    def wrap(func):
        def handle(signum, frame):  # 收到信号 SIGALRM 后的回调函数，第一个参数是信号的数字，第二个参数是the interrupted stack frame.
            raise RuntimeError

        def to_do(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)  # 设置信号和回调函数
                signal.alarm(num)  # 设置 num 秒的闹钟

                r = func(*args, **kwargs)

                signal.alarm(0)  # 关闭闹钟
                return r
            except RuntimeError as e:
                callback()

        return to_do

    return wrap

def error_handel():
    print("ERROR")

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

            sql = """INSERT INTO info_new(aid, tid, tname, pic, title, pubdate, description, duration, owner_mid, 
                        owner_name, view_num, danmaku, reply, favorite, coin, share_num, like_num, dislike)
                        VALUES (%(aid)s, %(tid)s, %(tname)s, %(pic)s, %(title)s, %(pubdate)s, %(description)s, %(duration)s, 
                        %(owner_mid)s, %(owner_name)s, %(view_num)s, %(danmaku)s, %(reply)s, %(favorite)s, %(coin)s, %(share_num)s, 
                        %(like_num)s, %(dislike)s);
                        """
            self.cursor.execute(sql, data)      # 防止sql注入
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(e)

            return e.args[0]

    # 插入数据, 接受参数 data = [{'aid' = xxx, 'tid' = xxx, .....}, ....]
    # @set_timeout(20, error_handel)
    def InsertManyData(self, data):

        try:

            sql = """INSERT INTO info_new(aid, tid, tname, pic, title, pubdate, description, duration, owner_mid, 
                        owner_name, view_num, danmaku, reply, favorite, coin, share_num, like_num, dislike)
                        VALUES (%(aid)s, %(tid)s, %(tname)s, %(pic)s, %(title)s, %(pubdate)s, %(description)s, %(duration)s, 
                        %(owner_mid)s, %(owner_name)s, %(view_num)s, %(danmaku)s, %(reply)s, %(favorite)s, %(coin)s, %(share_num)s, 
                        %(like_num)s, %(dislike)s);
                        """
            self.cursor.executemany(sql, data)  # 防止sql注入
            self.db.commit()
            return 0

        except Exception as e:
            print("[InsertManyData]")
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            if e.args[0] == 1062:
                print(e)
                self.db.commit()
                return 1062
            self.db.rollback()

            print(e)

            return e.args[0]


class BilibiliSprider:

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'api.bilibili.com',
        'Referer': 'https://www.bilibili.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    }

    # 单次线程池最大容量
    MAX_THREEDPOOL_SIZE = 10000

    # 最大出错数
    MAX_ERROR_TOLERATE = 100
    # 出错日志路径
    error_log_path = 'error_log' + str(int(time.time())) + '.txt'
    # 间隔时间
    SLEEP_TIME = 0.01
    # 数据暂存列表
    data_cache = []
    data_tmp_cache = []
    # 数据暂存列表容量
    MAX_DATA_CACHE_NUM = 1000
    # 总上传量
    total_insert = 0
    # 总需求量
    TARGET_NUM = 50000000

    def __init__(self, aids, thread_num=4):

        # 连接数据库
        self.db = DB(db_config)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("DB init!")

        # 初始化线程池
        self.executor = ThreadPoolExecutor(max_workers=thread_num)

        self.aids = aids

        # 出错的数量以及aid数
        self.error_num = 0
        self.error_aids = []

        # 互斥锁
        self.lock = Lock()
        self.tmp_cache_lock = Lock()

        # 起始aid 终止aid
        self.start_aid = start_aid
        self.end_aid = end_aid


    # 运行结束时，记录log
    def __exit__(self, exc_type, exc_val, exc_tb):
        f = open(self.error_log_path, 'w')
        f.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        f.write('\n')
        f.write(self.error_aids)
        f.close()

        print("Exit \ttime: ")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def __del__(self):
        print("Del \ttime: ")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def run(self):
        # self.executor.map(self.sprider, self.aids)
        self.executor.map(self.sprider_cache, self.aids)

    # Downloader 下载网页，获取数据
    def get_intro(self, aid):

        # something changed
        # url = 'https://api.bilibili.com/x/web-interface/archive/view?aid=' + str(aid)
        # url = 'https://api.bilibili.com/x/web-interface/view?aid=' + str(aid)
        # url = 'http://api.bilibili.com/x/web-interface/view?aid=' + str(aid)
        url = 'http://api.bilibili.com/x/web-interface/view/detail?aid=' + str(aid)

        req = requests.get(url, headers=self.headers, timeout=10)
        data_json = req.json()

        if req.status_code == 200:
            if data_json['code'] == 0:
                return data_json
            else:                           # 视频被删了or不存在
                return None
        else:
            print('[Error]\t%d\t%s', aid, req.status_code)
            print(req.text)
            return None

    def parse_json(data):
        dict = {
            'aid': data['aid'],
            'tid': data['tid'],
            'tname': data['tname'],
            'pic': data['pic'],
            'title': data['title'],
            'pubdate': data['pubdate'],
            'description': str(data['desc']).replace("\n", "  "),
            'duration': data['duration'],
            'owner_mid': data['owner']['mid'],
            'owner_name': data['owner']['name'],
            'view_num'  :data['stat']['view'],
            'danmaku'   :data['stat']['danmaku'],
            'reply'     :data['stat']['reply'],
            'favorite'  :data['stat']['favorite'],
            'coin'      :data['stat']['coin'],
            'share_num' :data['stat']['share'],
            'like_num'  :data['stat']['like'],
            'dislike'   :data['stat']['dislike']
            }
        return dict

    # Parser 解析数据中的字段，返回dict
    def parse_data(self, intro_json):
        dicts = []
        if intro_json:

            data = intro_json['data']

            # url = 'https://api.bilibili.com/x/web-interface/view/detail?aid=' + str(aid)
            data = data['View']

            if data['aid'] != 0:
                dict1 = parse_json(data)

                dicts.append(dict1)

                for related_vedio in intro_json['data']['Related']:
                    if related_vedio['aid'] != 0:
                        dict = parse_json(related_vedio)
                        dicts.append(dict)

                return dicts

        else:
            return None

    # Uploader 缓存数据并一次性上传至db
    def save_to_db_cache(self, dicts, aid):
        if aid:
            error_code = -1

            self.lock.acquire()                                 # 申请本地缓存读写锁
            if dicts:
                for dict_ in dicts:
                    if dict_['aid']:
                        self.data_cache.append(dict_)

            # cache数量达到阈值，上传至数据库
            if len(self.data_cache) >= self.MAX_DATA_CACHE_NUM or aid == self.end_aid:

                self.tmp_cache_lock.acquire()                   # 申请上传缓存读写锁
                self.data_tmp_cache = self.data_cache[:]        # 将本地缓存拷贝至上传缓存
                self.data_cache = []                            # 清空本地缓存
                self.lock.release()                             # 释放本地缓存读写锁

                time.localtime(time.time())

                # Insert and handle Exception
                error_code = self.db.InsertManyData(self.data_tmp_cache)
                if error_code == 0 or error_code == 1062:
                    self.total_insert += len(self.data_tmp_cache)
                    self.data_tmp_cache = []                    # 上传成功，清空上传缓存

                    self.tmp_cache_lock.release()               # 释放上传缓存读写锁

                    # 保存到文件中
                    f = open("current_aid.txt", "w")            # 将当前上传成功的aid写入文件，实现"断点续爬"
                    f.write(str(aid+1))
                    f.close()
                else:
                    print("[ERROR]\tdb insert error")
                    tmp = self.data_tmp_cache[:]
                    self.data_cache = self.data_cache + tmp
                    self.tmp_cache_lock.release()

            else:
                self.lock.release()                              # cache数量未达到阈值，直接释放本地缓存读写锁

            return error_code

    # Engine 线程入口点，控制Downloader、Parser、Uploader，并进行异常控制、处理
    def sprider_cache(self, aid):
        try:

            intro_json = self.get_intro(aid)

            if not intro_json:
                return

            dict = self.parse_data(intro_json)
#           # 播放数大于50000
            # if dict['view_num'] < 50000:
            #    return
            error_code = self.save_to_db_cache(dict, aid)
            if error_code == -1:
                pass
            else:
                if error_code == 1062:
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    print('[INFO]\tPRIMARY KEY Duplicate')
                elif error_code == 0:
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    print('[INFO]\t- %d\tsucc\ttotal: %d' % (aid, self.total_insert))
                else:
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    print('[ERROR]\t%d\tfail!' % aid)
                    self.error_handel(aid)

            # 控制访问频率
            time.sleep(self.SLEEP_TIME)
            return
        except requests.ConnectionError as e:
            print('[Error]\taid\t%s', e.args)
            self.aids.append(aid)           # 重试
            return

        except Exception as e:
            print("[sprider_cache]")
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            traceback.print_exc()
            print()
            if str(e) == "(0, '')":             # pymysql.err.InterfaceError: (0, '')  0号异常
                print("0 catch")
                # os.execv(__file__, sys.argv)
                python = sys.executable
                print(*sys.argv)
                os.execl(python, python, *sys.argv)
            self.error_handel(aid)


    # 存入db，主db、备份db
    def save_to_db(self, dict):
        if dict:
            self.lock.acquire()
            error_code = self.db.InsertData(dict)
            self.lock.release()
            if error_code:  # 主db、备份db同时写成功才返回true
                return True

        return False

    # 串联前三个func，并做判断，打log
    def sprider(self, aid):

        intro_json = self.get_intro(aid)
        if intro_json:

            dict = self.parse_data(intro_json)

#            # 播放数大于50000
            if dict['view_num'] < 50000:
                return

            error_code = self.save_to_db(dict)
            if error_code == 0:
                print('[INFO]\t%d\tsucc' % aid)
            else:
                if error_code == 1062:
                    print('[INFO]\tPRIMARY KEY Duplicate')
                else:
                    print('[ERROR]\t%d\tfail!' % aid)
                    self.error_handel(aid)

        # 控制访问频率
        time.sleep(self.SLEEP_TIME)

    # 错误达到一定数量，暂停并记录
    def error_handel(self, aid):
        self.error_num += 1
        self.error_aids.append(aid)

        if self.error_num > self.MAX_ERROR_TOLERATE:
            with open(self.error_log_path, 'w') as f:
                f.write(str(time.time()))
                f.write('\n')
                f.write(self.error_aids)
            exit(0)



if __name__ == '__main__':

    TARGET_NUM = 100000
    # start_aid = 40000000


    CURRENT_AID = 1

    if CURRENT_AID == 1:
        f = open("current_aid.txt")
        start_aid = int(f.read())
        print(start_aid)

    else:
        start_aid = 40000000

    end_aid = start_aid + 4000000

    aids = range(start_aid, end_aid)

    print("Begin \ttime: ")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    sprider = BilibiliSprider(aids, thread_num=30)
    sprider.run()
    # sprider.sprider(46263811)


