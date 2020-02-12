# -*- coding: utf-8 -*-
from myTool.RequestTool import requestForHtml
from myTool.findCheckTool import checkPatternList
from myTool.findCheckTool import findPattern
from myTool.RequestTool import downLoadPic

import os

def createDir(name):
    path = "/Users/ruixuandan/MyData/minne/" + name
    if not os.path.exists(path):
        os.makedirs(path)
    return path

if __name__ == "__main__":
    originURLTemplates = "https://minne.com/@petit-choco"
    # 第一页不用page参数
    text = requestForHtml(originURLTemplates)
    pagePattern = r'>(\d+?)</a></span><span class="next c-pagination__page items"'
    maxPage = checkPatternList(pagePattern, text)[0]
    for i in range(1, int(maxPage) + 1):
        url = originURLTemplates + "?page=" + str(i)
        text = requestForHtml(originURLTemplates)
        listItemPattern = r'<div class="galleryProductList__item" .*?>.*?</div></div></div></div>'
        itemList = checkPatternList(listItemPattern, text)
        picPath = createDir("第" + str(i) + "页")
        for itemText in itemList:
            itemPattern = r'<div class="galleryProductList__item" data-product_id=".*?">.*data-product-price="(.*?)".*data-bg="(.*?)">.*data-product-name="(.*?)"'
            item = findPattern(itemPattern, itemText)
            
            productPrice = item[0]
            productBg = "https:" + item[1]
            productName = item[2].replace(u'\u3000', " ") + "___" + productPrice + "円"
            
            print(productPrice + "==" + productBg + "==" + productName)
            
            downLoadPic(picPath, productName, productBg)