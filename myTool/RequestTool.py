# -*- coding: utf-8 -*-
from urllib import request

def requestForHtml(url):
    req = request.Request(url)
    html = request.urlopen(req)
    return html.read().decode("euc-jp")

def downLoadPic(dirPath, name, Addr):
    request.urlretrieve(Addr, dirPath + "/" + name + ".jpg")