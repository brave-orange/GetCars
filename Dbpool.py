#!/usr/bin/env python
# encoding=utf-8
import pymysql,time, threading
class Dbpool:
    # minfree:最小空闲数，空闲小于此则创建，maxfree:反之，maxlinks:最大链接数
    
    def __init__(self,host,port,username,password,dbname,minfree = 5,maxfree = 15,maxlinks = 20):
        self.minfree = minfree
        self.maxfree = maxfree
        self.maxlinks = maxlinks
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname
        self.links_used = []
        self.free_link = []
        self.lock = threading.Lock()
        self.create_new_freelink(self.minfree)
        
    def getLinks(self):
        return self.free_link
    def getUsedLinks(self):
        return self.links_used

    def create_new_freelink(self,num):
        for i in range(num):
            mysql = pymysql.connect(self.host,self.username,self.password,self.dbname,charset="utf8")
            self.free_link.append([mysql,time.time()])

    def destory_freelink(self):
        print("destory_freelink")
        mysql = self.free_link.pop(0)
        mysql.close()

    def destory_usedlink(self,index):    #链接用完放到空闲链接中
        mysql = self.links_used.pop(index)
        if len(self.free_link) < self.maxfree:
            self.free_link.append(mysql[0])
        else:
            mysql.close()

    def getConnection(self):  #pid 线程id
        self.checkPool()
        now = time.time()
        if len(self.links_used) > self.maxlinks:
            print("链接满了%d" % len(self.links_used))
            while 1:
                time.sleep(20)
                if len(self.links_used) < self.maxlinks:
                        break
                if time.time() > now + 600:
                    return None     #连接池满等待超时
        link = self.getFreelink()
        self.checkPool()
        return link

    def checkPool(self):
        if len(self.free_link) < self.minfree:
            self.create_new_freelink(self.minfree-len(self.free_link))
        elif len(self.free_link) > self.maxfree:
            self.destory_freelink()

    def getFreelink(self):
        p = self.getpid()
        conn = self.free_link.pop(0)    #队列结构
        self.links_used.append([conn,p])
        return conn[0]

    def Commplete(self):
        t = threading.currentThread()
        self.lock.acquire() 
        for i in  range(len(self.links_used)):
            if self.links_used[i][1] == self.getpid():
                self.destory_usedlink(i)
                break
        self.lock.release()
        print("释放一个链接，当前freelink:%d,links_used:%d" % (len(self.free_link),len(self.links_used)))
        self.checkPool()
    def getpid(self):
        t = threading.currentThread()
        return t.ident




