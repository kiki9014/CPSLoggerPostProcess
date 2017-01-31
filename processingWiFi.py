import importEncodedData as iED
import os.path
import pickle
import numpy as np
import scipy.io as sio

dateFile = "2016_05_18"

name = "GalaxyS7"

type = "Wifi"

path = "D:/SmartCampusData" + "/" + name + "/CPSLogger/" + type

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
        table[data] = len(table)
        return table[data]

def processingAP(data, table) :
    fragment = data.split(",")
    # print(fragment)
    id = hashing(fragment[0], table)
    if len(fragment) < 5 :
        return [-1, -1, -1]
    freq = int(fragment[-2])
    # if fragment[-1] == '-v' : print(ts)
    lev = int(fragment[-1])
    result = [id, freq, lev]
    return result

tableTemp = loadHashTable("BSSID")
if tableTemp == "null" :
    table = dict()
else :
    table = tableTemp

# directoryPath = "D:/Data/"
#
# name = "P1"
#
# pathd = directoryPath + name + "/CPSLogger/" + type
#
# fileList = [f for f in os.listdir(pathd) if os.path.isfile(os.path.join(pathd, f))]
#
# for f in fileList:
#     dateFile = f[-14:-4]
#     # print(dateFile[5:7])
#     print(dateFile)
#     timeStamp, data = iED.extract(directoryPath, name, type, dateFile, True)
#     if len(data) == 0:
#         continue
#     if dateFile == "2017_01_10" :
#         print(data)
#     temp = [processingAP(dataF, table, timeStamp[np.where(data == dataF)]) for dataF in data]
#     iED.saveTomat(type, dateFile, timeStamp, temp, name)

# iED.saveTomat("Wifi",date,timeStamp,data,name)

# fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#
# for f in fileList :
#     dateFile = f[-14:-4]
#     # print(dateFile[5:7])
#     if int(dateFile[5:7]) < 5 :
#         continue
#     print(dateFile)
#     timeStamp, data = iED.extract(name, type, dateFile, True)
#     if len(data) == 0:
#         continue
#     temp = [processingAP(dataF, table) for dataF in data]
#     iED.saveTomat(type, dateFile, timeStamp, temp, name)
# saveHashTable(table, "BSSID")