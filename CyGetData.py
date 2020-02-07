# -*- coding: utf-8 -*-

import os
from myTool.RequestTool import requestForHtml
from myTool.RequestTool import downLoadPic
from myTool.findCheckTool import findPattern
from myTool.findCheckTool import checkPatternList

def createDir(name):
    path = "/Users/ruixuandan/MyData/cy/" + name
    if not os.path.exists(path):
        os.makedirs(path)
    return path
  
def getProductList(cbid):
    url = "https://cyanic-nature.com/?mode=cate&cbid=" + cbid + "&csid=0"
    return requestForHtml(url)

def getDetail(pid):
    url = "https://cyanic-nature.com/" + pid
    return requestForHtml(url)
    
if __name__ == "__main__":
    hpHtml = requestForHtml("https://cyanic-nature.com/")
    
    findOption = findPattern(r'<select class="prd_search_select" name="cid">[\s\S]*</select>', hpHtml)
    findOption = findPattern(r'<option\s?value=".+">[\s\S]*</option>', findOption)
    findOptionList = checkPatternList(r'<option .*?>.*?</option>', findOption)
    for item in findOptionList:
        valuePattern = r'<option value="(.*),0">(.*)</option>'
        result = checkPatternList(valuePattern, item)
        for t in result:
            print("商品类型：" + str(t[1]))
            
            localSaveDir = createDir(str(t[1]))
            result = getProductList(t[0])
            # 开始解析商品列表页
            findUl = findPattern(r'<ul class="prd_lst prd_lst_s clearfix">[\s\S]*?</ul>', result)
            findUlList = checkPatternList(r'<li class="prd_lst_unit prd_lst_unit_s">[\s\S]*?href="(.*?)"[\s\S]*?<img src="(.*?)".*?alt="(.*?)"', findUl)
            for i in findUlList:
                pid = i[0]
                picAddr = i[1]
                productName = i[2]
                # 消除新商品商品名中的<img>标签
                suffixIndex = i[2].find("<img")
                if suffixIndex > 0:
                    productName = productName[:suffixIndex]
                # 消除商品名中影响目录的斜杠
                productName = productName.replace("/", ":")
                # 获取商品详细信息页面
                detailResult = getDetail(pid)
                findTable = findPattern(r'<table class="product_spec_table none_border_table">[\s\S]*?<td>(.*?)</td>', detailResult)
                # 下载高清图片
                picAddr = picAddr.replace("_th", "")
                downLoadPic(localSaveDir, findTable + "__" + productName, picAddr)