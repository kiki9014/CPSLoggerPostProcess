from lxml import html
import requests
import numpy as np
import scipy.io as sio
import pickle
import os.path

# appTable = {}
# categoryList = []

def loadHashTable(tableName) :
    if not os.path.isfile(tableName + ".pkl") :
        return "null"
    with open(tableName + ".pkl", 'rb') as f :
        return pickle.load(f)

def saveHashTable(obj, tableName) :
    with open(tableName + ".pkl", 'wb') as f :
        pickle.dump(obj,f)

def loadTable () :
    totalTable = loadHashTable("AppCategory")
    if totalTable != "null" :
        categoryList = totalTable["categoryList"]

        appTable = totalTable

        del appTable["categoryList"]
    else :
        categoryList = []
        appTable = {}
    return appTable, categoryList

appTable, categoryList = loadTable()

androidMarketUrl = "https://play.google.com/store/apps/details?id="

def requestCategory(appName) :
    page = requests.get(androidMarketUrl + appName)
    tree = html.fromstring(page.content)
    parsed = tree.xpath('//span[@itemprop="genre"]/text()')

    if len(parsed) != 0 :
        category = parsed[0].encode('ISO-8859-1').decode('UTF-8')
    else :
        category = "etc"

    # print(category)
    return category

def getCategory(appName) :
    for cat in appTable :
        if appName in appTable[cat] :
            return categoryList.index(cat)

    newCat = requestCategory(appName)

    if newCat in appTable :
        appTable[newCat].append(appName)
    else :
        appTable[newCat] = [appName]
        categoryList.append(newCat)

    return categoryList.index(newCat)

def saveTable () :
    totalTable = appTable
    totalTable["categoryList"] = categoryList

    saveHashTable(totalTable, "AppCategory")

# cat1 = requestCategory("jp.grenge.pocolondungeons,com")
# # cat2 = getCategory("jp.naver.line.android")
# #
# # cat3 = getCategory("com.chineseskill")
# #
# print(cat1)
# # print(cat2)
# # print(cat3)
# #
# print(categoryList)
# print(appTable)
#
# saveTable()