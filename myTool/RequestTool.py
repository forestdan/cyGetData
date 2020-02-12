# -*- coding: utf-8 -*-
from urllib import request

def requestForHtml(url, decode = "utf-8"):
    """
    请求URL,decode为解码方式
    """
    req = request.Request(url)
    html = request.urlopen(req)
    return html.read().decode(decode)

def downLoadPic(dirPath, name, Addr):
    """
    下载图片
    """
    request.urlretrieve(Addr, dirPath + "/" + name + ".jpg")