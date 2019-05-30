#!/usr/bin/env python
# encoding=utf-8
import requests
from pyquery import PyQuery
from Dbpool import *
from RedisDb import *
import chardet,re,pymysql,time,json

pool = Dbpool("localhost", "3306", "root", "root", "test1")
redis = RedisDb("localhost", 6379)
def GetHtml(url):
    print("正在获取%s页面---"%url)
    r = requests.get(url)
    return r
def GetBrandsPage(start):
    mysql = pool.getConnection()
    sql ="select count(1) from brands"
    cursor = mysql.cursor()
    try:
       # 执行sql语句
        cursor.execute(sql)
        res = cursor.fetchall()
        count = res[0][0]
    except:
       # 发生错误时回滚
       mysql.rollback()
    if start > count:
        return False
    sql = "select url,brand from brands limit %s , 10"%start
    #sql = "select url,brand from brands"
    try:
        cursor.execute(sql)
        res = cursor.fetchall()
        res_data = []
        for i in res:
            res_data.append([i[0],i[1]])
        mysql.close()
        return res_data
    except:
       # 发生错误时回滚
       mysql.rollback()
    pool.Commplete()


def insertCars(cars,brand):
    for car in cars:
        car["brand"] = brand
        car_json = json.dumps(car)
        redis.lpush("cars",car_json)
    return True
def GetpageUrl(pages):  #获取分页信息
    p = PyQuery(pages)
    target_urls = []
    for item in p("a"):
        qitem = PyQuery(item)
        if qitem.text() == "上一页" or qitem.text() == "下一页"  or qitem.attr("href") == "javascript:void(0);":
            continue
        target_urls.append("https://car.autohome.com.cn"+qitem.attr("href"))
    return target_urls

def getcars(car_page,brand):
    car_ul = PyQuery(car_page)("div .list-cont-bg")
    cars = []
    for car_item in car_ul:
        car = {}
        car_p = PyQuery(car_item)
        car["img"] = "https://"+car_p.find(".list-cont-img").find("img").attr("src")
        main_title = car_p.find("div .main-title")
        car["car_name"] = main_title.find("a").text()
        car["score"] = main_title.find("span").text().strip(" ");
        main_title = car_p.find("div .main-lever-left")
        car["price"] = car_p.find(".lever-price").text()
        title_li = PyQuery(main_title).find("li")
        car["type"] = PyQuery(title_li[0]).find("span").text()
        car["car_body"] = PyQuery(title_li[1]).find("a").text()
        car["engine"] = PyQuery(title_li[2]).find("span").text()
        car["gearbox"] = PyQuery(title_li[3]).find("a").text()
        cars.append(car)
    insertCars(cars,brand)
    print("抓取%s完成，写入Redis完成"%brand)



def GetCarsdata(urls):
    for url in urls:
        print("抓取：%s"%url[0])
        r = GetHtml(url[0])
        doc = PyQuery(r.text)
        getcars(r.text,url[1]) #第一页
        pages = doc("div .price-page")
        if pages:
            data = GetpageUrl(pages)
            print(data)
            for i in data:
                car_page = GetHtml(i)
                getcars(car_page.text,url[1])
                # time.sleep(5)
    print("结束一个线程")

count = 215
for i in range(int(count/10)+1):
    start = i*10 
    print(start)
    urls = GetBrandsPage(start)
    if not urls:
        print("没有目标地址")
        continue
    t = threading.Thread(target=GetCarsdata, args=(urls,))
    print("开启线程：%d"%i)
    t.start()
    t.join()
    # time.sleep(5)
print("抓取完成")

