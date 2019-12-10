#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/8/18 11:37
# @File    : Picture.py
import pymysql
import sys
from TCPServer import *
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

#conn = mysql.connect(host='localhost', user='root', passwd='xxx', db='mydata')

fp = open("6a0f060cf95601d3e8f562670dd21788.jpg",'rb')
img = fp.read()
fp.close()


# 存入图片
def insert_imgs(img):
    # mysql连接

    cursor = mydb.cursor()
    # 注意使用Binary()函数来指定存储的是二进制
    # cursor.execute("insert into img set imgs='%s'" % mysql.Binary(img))
    cursor.execute("Insert into images values(%s,%s)", ("6a0f060cf95601d3e8f562670dd21788.jpg",pymysql.Binary(img)))
    # 如果数据库没有设置自动提交，这里要提交一下
    mydb.commit()
    cursor.close()
    # 关闭数据库连接
    mydb.close()


# 提取图片
def select_imgs():
    cursor = mydb.cursor()
    cursor.execute('select * from images')
    s = cursor.fetchall()
    print(s[0][0])
    fp=open('1.jpg','wb')
    fp.write(s[0][1])
    fp.close()
    img = cv2.imdecode(np.frombuffer(s[0][1], np.uint8), cv2.IMREAD_COLOR)
    # # 将bgr转为rbg
    rgb_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    print(rgb_img)
    # np.ndarray转IMAGE
    a = Image.fromarray(rgb_img)
    print(a)
    a.show()
    # 显示图片
    cursor.close()
    mydb.close()
#insert_imgs(img)
select_imgs()
server.stop()