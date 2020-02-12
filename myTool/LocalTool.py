# -*- coding: utf-8 -*-
import os

myDataPath = "/Users/ruixuandan/MyData/"

def createDir(siteName, name):
    """
    创建本地目录
    返回创建目录路径
    """
    path = myDataPath + siteName + "/" + name
    if not os.path.exists(path):
        os.makedirs(path)
    return path