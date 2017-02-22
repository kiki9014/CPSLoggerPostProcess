import os.path
import pickle

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
    id = hashing(fragment[0], table)
    if len(fragment) < 5 :
        return [-1, -1, -1]
    freq = int(fragment[-2])
    lev = int(fragment[-1])
    result = [id, freq, lev]
    return result

tableTemp = loadHashTable("BSSID")
if tableTemp == "null" :
    table = dict()
else :
    table = tableTemp
