#!/usr/bin/env python
# encoding=utf-8
import pymysql,time
class Dbpool:
    # minfree:最小空闲数，空闲小于此则创建，maxfree:反之，maxlinks:最大链接数
    
    def __init__(self,host,port,username,password,dbname,minfree = 5,maxfree = 15,maxlinks = 20):
        self.minfree = minfree
        self.maxfree = maxfree
        self.maxlinks = maxlinks
        self.links_used = []
        self.free_link = []
        for i in range(minfree-1):
            self.create_new_freelink()
        
    def getLinks(self):
        return self.free_link

    def create_new_freelink(self):
        mysql = pymysql.connect(host,username,password,dbname,charset="utf8")
        self.free_link.append([mysql,time.time()])

    def destory_freelink(self,index):
        mysql = self.free_link.pop(index)
        mysql.close()

    def getConnection(self):
        if len(self.free_link) < self.minfree:
            self.create_new_freelink()
        conn = self.free_link.pop()
        return conn



