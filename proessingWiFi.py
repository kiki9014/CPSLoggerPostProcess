import importEncodedData as iED
import os.path
import pickle
import scipy.io as sio

dateFile = "2016_05_18"

name = "Iron2"

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
    lev = int(fragment[-1])
    result = [id, freq, lev]
    return result

tableTemp = loadHashTable("BSSID")
if tableTemp == "null" :
    table = dict()
else :
    table = tableTemp

# timeStamp, data = iED.extract(name, "Wifi", date, True)

# print(data[0])
# print(data)

# temp = [processingAP(dataF, table) for dataF in data]

# print(processingAP(data[0],table))

# iED.saveTomat("Wifi",date,timeStamp,data,name)

fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for f in fileList :
    dateFile = f[-14:-4]
    # print(dateFile[5:7])
    if int(dateFile[5:7]) < 5 :
        continue
    print(dateFile)
    timeStamp, data = iED.extract(name, type, dateFile, True)
    if len(data) == 0:
        continue
    temp = [processingAP(dataF, table) for dataF in data]
    iED.saveTomat(type, dateFile, timeStamp, temp, name)
saveHashTable(table, "BSSID")