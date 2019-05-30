#!/usr/bin/env python
# encoding=utf-8
import redis

class RedisDb:
    def __init__(self,host,port,):
        self.pool = redis.ConnectionPool(host=host , port=port, decode_responses=True)
        
    def lpush(self,name,data):
        conn = redis.Redis(connection_pool=self.pool)
        conn.lpush(name,data)
    def lrange(self,name,start,stop):
        conn = redis.Redis(connection_pool=self.pool)
        res = conn.lrange(name,start,stop)
        return res
