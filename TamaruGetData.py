# -*- coding: utf-8 -*-
from myTool.RequestTool import requestForHtml
from myTool.findCheckTool import checkPatternList
from myTool.findCheckTool import findPattern
from myTool.LocalTool import createDir, myDataPath
from myTool.RequestTool import downLoadPic
import os
import xlsxwriter

siteName = "Tamaru"
# 所需要的种类
needs = "生き物、植物、道具・アイテム、自然、人物・キャラクター、文字、言葉、正月、家紋、ミニスタンプ"

xlsxHead = ("序号", "大分类", "小分类", "日文名称", "图片", "售价", "尺寸", "链接")

sitePageHomeUrl = "https://tamaru-online.com"

def getDetail(url):
    """
    获取商品详情页有用信息
    """
    mi = requestForHtml(sitePageHomeUrl + url)
    miNamePattern = r'<h1 class="product-item-caption-title -product-page">(.*?)</h1>'
    miPricePattern = r'<span class="money" itemprop="price" content=".*?">(.*?)</span>'
    miImgPattern = r'<img class="product-item-img[\s\S]*?data-src="(.*?)"'
    miSizePattern = r'サイズ：(.*?)\(縦×横×高さ\)'
    
    name = findPattern(miNamePattern, mi).replace("\u3000", " ")
    price = findPattern(miPricePattern, mi).replace("¥", "")
    imgi = findPattern(miImgPattern, mi)
    img = ""
    if not imgi == None:
        img = "https:" + findPattern(miImgPattern, mi).replace("{width}", "300")
    size = findPattern(miSizePattern, mi)
    return (name, img, price, size)

if __name__ == "__main__":
    print("开始爬取数据")
    mainListUrl = sitePageHomeUrl + "/pages/kyoufufu"
    mainListHtml = requestForHtml(mainListUrl)
    mainListPattern = r'<a class="gallery-item-link" href="(.*?)" title="(.*?)" data-subtitle=""></a>'
    mainList = checkPatternList(mainListPattern, mainListHtml)
    collectionsList = []
    productInfoList = []
    """
    生成文档目录结构 (主类， 小类， collections地址)
    """
    for mainListItem in mainList:
        if needs.find(mainListItem[1]) < 0:
            continue
        if mainListItem[0].find("/pages") < 0:
            collectionsList.append((mainListItem[1], "無し", mainListItem[0]))
        else:
            subListUrl = sitePageHomeUrl + mainListItem[0]
            subListHtml = requestForHtml(subListUrl)
            subListPattern = r'<a class="collection-thumb-link" href="(.*?)">[\s\S]*?<h5 class="collection-thumb-title text-normal">(.*?)</h5>'
            subList = checkPatternList(subListPattern, subListHtml)
            for subListItem in subList:
                collectionsList.append((mainListItem[1], subListItem[1], subListItem[0]))

    """
    生成每个商品数据，存于tuple中
    """
    index = 0
    print("开始获取详情数据")
    for collection in collectionsList:
        collectionHtml = requestForHtml(sitePageHomeUrl + collection[2])
        collectionPattern = r'<a class="product-thumb-href" href="(.*?)"></a>'
        productList = checkPatternList(collectionPattern, collectionHtml)
        for item in productList:
            index += 1
            # 与报表中一致
            productInfo = (index,) + collection[0:2] + getDetail(item) + (item, )
            print(productInfo)
            productInfoList.append(productInfo)
    print("详情数据获取结束")
    print("开始生成Excel")
    """
    开始生成Excel
    """
    xlsxPath = myDataPath + siteName + "test.xlsx"
    
    workbook = xlsxwriter.Workbook(xlsxPath)
    worksheet = workbook.add_worksheet()
    
    row = 0
    col = 0
    # 生成表头
    for count in range(0, len(xlsxHead)):
        worksheet.write(row, col + count, xlsxHead[count])
    row +=1
    # 插入数据
    for productInfo in productInfoList:
        dirPath = createDir(siteName, productInfo[1] + "/" + productInfo[2])
        picPath = ""
        if not productInfo[4] == "":
            picPath = downLoadPic(dirPath, str(productInfo[0]), productInfo[4])[0]
        worksheet.write(row, col, productInfo[0])
        worksheet.write(row, col + 1, productInfo[1])
        worksheet.write(row, col + 2, productInfo[2])
        worksheet.write(row, col + 3, productInfo[3])
        if not picPath == "":
            worksheet.insert_image(row, col + 4, picPath, {'x_scale': 0.3, 'y_scale': 0.25})
        worksheet.write(row, col + 5, productInfo[5])
        worksheet.write(row, col + 6, productInfo[6])
        worksheet.write(row, col + 7, sitePageHomeUrl + productInfo[7])
        row += 1
    workbook.close()
    print("生成结束")