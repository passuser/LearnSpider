#!/usr/bin/env python3                          
# -*- coding:utf-8 -*-                          
#     Author : goorwt@gmail.com                 
#   File Name:save.py
#Created Time:2018-09-16
#################################################
'''
储存图片，输入目录绝对路径
'''
import time,os
class save(object):
    def __init__(self):
        self.i = 0
        self.ospath = input('输入储存目录绝对路径：')
        if os.path.exists(self.ospath):
            pass
        else:
            print('该路径不存在或路径名错误！')

    def img_save(self,img,filepath):
        if filepath:
            filepath = self.ospath + '/' + filepath 
            if os.path.exists(filepath):
                with open(filepath+'/'+'%s'%int(time.time())+'.jpg','wb') as f:
                    if img:
                        f.write(img.content)
                        self.i = self.i + 1
                        print('已爬取%d张图片'%self.i)
                    else:
                        print('未下载到图片')
            else :
                os.mkdir(filepath)
                with open(filepath+'/'+'%s'%int(time.time())+'.jpg','wb') as f:
                    if img:
                        f.write(img.content)
                        self.i = self.i + 1
                        print('已爬取%d张图片'%self.i)
                    else:
                        print('未下载到图片')
