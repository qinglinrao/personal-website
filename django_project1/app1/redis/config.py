#!/usr/bin/env python3
#coding:utf8

import redis
class Redis(object):

    host = 'localhost123'
    port = 6379
    redis_link = None

    def link(self):
        # self.redis_link = redis.Redis(host=self.host, port=self.port, password='foobared_kami2018')
        self.redis_link = redis.Redis(host=self.host, port=self.port)
        print(self.redis_link)
        # r = redis.StrictRedis(host='0.0.0.0', port=6379)
        # 如果要指定数据库，则 r = redis.StrictRedis(host='0.0.0.0', port=6379, db=0)

    def set(self, key, value, time=None):
        if not key:
            return

        if time:
            self.redis_link.set(key, value, time)
        else:
            self.redis_link.set(key, value)

    def get(self, key):
        if not key:
            return
        return self.redis_link.get(key)
