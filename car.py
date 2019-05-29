#!/usr/bin/env python
# encoding=utf-8
import requests
from pyquery import PyQuery
from Dbpool import *
import chardet,re,pymysql,time

pool = Dbpool("localhost", "3306", "root", "root", "test1")

def GetHtml(url):
    print("正在获取%s页面---"%url)
    r = requests.get(url)
    return r

def GetBrands():

    mysql = pool.getConnection()
    url = "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0"
    r = GetHtml(url)
    doc = PyQuery(r.text)
    cartree = doc('.cartree')
    cursor = mysql.cursor()
    count = 0
    for pp in doc("ul"):
        pp1 = PyQuery(pp)
        for zipp in pp1('li'):
            a = PyQuery(zipp).find("a")
            title = a.html()
            title =  re.findall("/>(.*)<em>",title)
            number = PyQuery(zipp).find("a").find("em").html()
            number =  re.findall("[(](.*)[)]",number)
            a = 'https://car.autohome.com.cn'+a.attr("href")
            
            sql = "insert into brands (brand,count,url) values('%s','%s','%s')"%(title[0],number[0],a)
            try:
               # 执行sql语句
               cursor.execute(sql)
               # 执行sql语句
               mysql.commit()
               count = count + 1
            except:
               # 发生错误时回滚
               mysql.rollback()
             
            # 关闭数据库连接
    pool.Commplete()
    return count

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


def insertCars(cars,brand,mysql):

    cursor = mysql.cursor()
    for car in cars:
        sql = "insert into cars (car_name, sorce, type, engine, car_body, gearbox, price, img,brand) VALUES ('%s', '%s','%s','%s','%s','%s','%s','%s','%s')"%(car["car_name"],car["score"],car["type"],car["engine"],car["car_body"],car["gearbox"],car["price"],car["img"],brand)

        try:
            cursor.execute(sql)
            mysql.commit()
           
        except:
           # 发生错误时回滚
           mysql.rollback()
    # mysql.close()
    
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

def getcars(car_page,url):
    mysql = pool.getConnection()
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
    insertCars(cars,url,mysql)
    print("抓取%s完成，写入数据库完成"%url)
    pool.Commplete()



def GetCarsdata(urls):
    for url in urls:
        print("抓取：%s"%url[0])
        r = GetHtml(url[0])
        doc = PyQuery(r.text)
        t = threading.Thread(target=getcars, args=(r.text,url[1],))
        print("开启抓车子线程")
        t.start()
        time.sleep(2)
        pages = doc("div .price-page")
        if pages:
            data = GetpageUrl(pages)
            print(data)
            for i in data:
                car_page = GetHtml(i)
                t = threading.Thread(target=getcars, args=(car_page.text,url[1],))
                print("开启抓车子线程")
                t.start()



# count = GetBrands()
# 
count = 215
for i in range(int(count/5)+1):
    start = i*5 
    print(start)
    urls = GetBrandsPage(start)
    if not urls:
        print("没有目标地址")
        break;
    t = threading.Thread(target=GetCarsdata, args=(urls,))
    print("开启线程：%d"%i)
    t.start()
    t.join()
# print("抓取完成")

