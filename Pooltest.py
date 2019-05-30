#!/usr/bin/env python
# encoding=utf-8
from Dbpool import *
from RedisDb import *
import threading
# mysql = Dbpool("localhost", "3306", "root", "root", "test")
redis = RedisDb("localhost", 6379)
redis.lpush("cars", "2142141gfghrf24")
redis.lpush("cars", "2142141gfghrf24")
redis.lpush("cars", "2142141gfghrf24")
print(redis.lrange("cars",0,-1))
# def test():
#     mysql.getConnection()
#     # print (a)
#     #t = threading.currentThread()
#     # print(t.ident)
#     # # print("-------------all----------------")
#     # print(mysql.getLinks())
#     # print("--------------free---------------")
#     # print(mysql.getUsedLinks())
#     # print("---------------used--------------")
#     t = threading.currentThread()
#     print(t.ident)
#     mysql.Commplete()



# for i in range(5):
#     t = threading.Thread(target=test, args=())
#     t.start()
#     t.join()

# print (a)
# print("-----------------------------")
# print(mysql.getLinks())
# print("-----------------------------")
# print(mysql.getUsedLinks())
# print("-----------------------------")
