# -*- coding: utf-8 -*-
import re

def checkPatternList(pattern, str):
    return re.compile(pattern).findall(str)

def findPattern(pattern, str):
    textList = checkPatternList(pattern, str)
    if len(textList) == 0:
        return None
    return textList[0]