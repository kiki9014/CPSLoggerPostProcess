import numpy as np
import scipy.io as sio
import os.path
import pickle
import numpy.matlib as npmlib
import appCategory
import sys

directoryPath = "D:/SmartCampusData"

blackList = ["cpslab.inhwan.cpslogger_v02", "com.android.browser","com.android.dialer", "com.bnl.GanadaIMEBeta", "com.buzzpia.aqua.launcher", "kvp.jjy.MispAndroid320", "com.google.android.wearable.app"]

messengerList = ['com.kakao.talk','jp.naver.line.android','com.Slack','com.facebook.orca']

count = {}

def initCount(nameList) :
    count = {}
    for name in nameList :
        count[name] = {'app' : {}, 'category' : {}}
    return count

def loadHashTable(tableName) :
    if not os.path.isfile(tableName + ".pkl") :
        return "null"
    with open(tableName + ".pkl", 'rb') as f :
        return pickle.load(f)

def saveHashTable(obj, tableName) :
    with open(tableName + ".pkl", 'wb') as f :
        pickle.dump(obj,f, pickle.HIGHEST_PROTOCOL)

def hashing(data, table) :
    if data in table :
        return table[data]
    else :
        table[data] = len(table)+1
        return table[data]

def countApp (name, app, category) :
    if app in count[name]["app"] :
        count[name]["app"][app] += 1
    else :
        count[name]["app"][app] = 1

    if category in count[name]["category"] :
        count[name]["category"][category] += 1
    else :
        count[name]["category"][category] = 1

def saveCount(nameList) :
    appCnt = {}
    catCnt = {}
    for name in nameList :
        appCnt[name] = list(count[name]["app"].items())
        catCnt[name] = list(count[name]["category"].items())

    sio.savemat("../common/appCount.mat", appCnt)
    sio.savemat("../common/categoryCount.mat", catCnt)

def processingApp(name, data, table):
    category = appCategory.getCategory(data)

    hashedApp = hashing(data, table)

    countApp(name,hashedApp,category)

    if data in messengerList :
        return [hashedApp, 1, category]
    else :
        return [hashedApp, 0, category]

def initAppProcessing(list):
    return initCount(list)

def extractAndSave(path, name, type, date) :
    tableTemp = loadHashTable("AppTable")
    if tableTemp == "null" :
        table = dict()
    else :
        table = tableTemp
    flag = False

    try :
        with open(path + "/" + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f :

            while True :
                line = f.readline().rstrip('\n')

                if not line: break
                if line[len(line) - 1] == ',': break
                if line[len(line) - 1] == '-': break
                if line[len(line) - 1] == '.': break

                dataF = line.split(",")

                time = [[float(timeChunk) for timeChunk in dataF[0:3]]]

                parsed = [processingApp(name, dataChunk,table) for dataChunk in dataF[4:] if not dataChunk in blackList]
                # print(parsed)

                if not flag:
                    data = np.array([parsed])
                    # timeStamp = np.array(time)
                    timeStamp = npmlib.repmat(time, len(parsed), 1)
                    flag = True
                else:
                    data = np.append(data, [parsed])
                    repTime = npmlib.repmat(time, len(parsed), 1)
                    # print(repTime)
                    timeStamp = np.append(timeStamp, repTime, axis=0)
    except IOError as error :
        print("Error occurred when processing App History : {0}".format(error))
    except :
        print("Unexpected error occurred : " + sys.exc_info()[0])
    if not os.path.exists("../" + name):
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + type):
        os.mkdir("../" + name + "/" + type)
    if not flag :
        flag = True
        timeStamp = np.array([])
        data = np.array([])
    if flag :
        sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat", {"timeStamp_" + type : timeStamp, type: data})

    saveHashTable(table, "AppTable")
    # print(table)

# phoneList = ["Iron2", "GalaxyS6", "GalaxyS7", "Vu2", "G5", "Nexus5X"]
# #
# phoneList = ["P1", "P2", "P3", "P4"]
# # type = "App"
# #
# count = initCount(phoneList)
# tableTemp = loadHashTable("AppTable")
# print(tableTemp)
#
# for name in phoneList :
#     # name = "Iron2"
#
#     path = "D:/SmartCampusData" + "/" + name + "/CPSLogger/" + type
#
#     fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#
#     for f in fileList :
#         dateFile = f[-14:-4]
#         # print(dateFile[5:7])
#         if int(dateFile[5:7]) < 5 :
#             continue
#         print(dateFile)
#         extractAndSave(directoryPath, name, type, dateFile)

# # print(table)
# appCategory.saveTable()
# saveCount(phoneList)

# extractAndSave("GalaxyS6", type, "2016_09_22")