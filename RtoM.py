#!/usr/bin/env python
# encoding=utf-8
from RedisDb import *
from Dbpool import *
import json
pool = Dbpool("localhost", "3306", "root", "root", "test1")
redis = RedisDb("localhost", 6379)

def insertCars(cars):
    print("插入一行")
    mysql = pool.getConnection()
    cursor = mysql.cursor()
    for car in cars:
        car = json.loads(car)
        sql = "insert into cars (car_name, sorce, type, engine, car_body, gearbox, price, img,brand) VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s')"%(car["car_name"],car["score"],car["type"],car["engine"],car["car_body"],car["gearbox"],car["price"],car["img"],car["brand"])
        try:
            cursor.execute(sql)
            mysql.commit()
           
        except:
           # 发生错误时回滚
           
           mysql.rollback()
    print("插入一行结束")
    pool.Commplete()
    

len = redis.llen("cars")
for i in range(int(len/20)+1):
    start = i*20
    stop = start + 19
    cars = redis.lrange("cars", start, stop)
    t = threading.Thread(target=insertCars, args=(cars,))
    print("开启线程：%d"%i)
    t.start()
    t.join()