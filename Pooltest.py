#!/usr/bin/env python
# encoding=utf-8
from Dbpool import *
mysql = Dbpool("localhost", "3306", "root", "root", "test")
print(mysql.getLinks())