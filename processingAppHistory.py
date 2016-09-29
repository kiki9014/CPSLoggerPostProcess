import numpy as np
import scipy.io as sio
import os.path
import pickle
import numpy.matlib as npmlib

directoryPath = "D:/SmartCampusData"

blackList = [""]

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

def extractAndSave(name, type, date) :
    tableTemp = loadHashTable("AppTable")
    if tableTemp == "null" :
        table = dict()
    else :
        table = tableTemp

    with open(directoryPath + "/" + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f :
        flag = False

        while True :
            line = f.readline().rstrip('\n')

            if not line: break
            if line[len(line) - 1] == ',': break
            if line[len(line) - 1] == '-': break
            if line[len(line) - 1] == '.': break

            dataF = line.split(",")

            time = [[float(timeChunk) for timeChunk in dataF[0:3]]]

            parsed = [hashing(dataChunk,table) for dataChunk in dataF[4:]]
            print(parsed)

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

        if not os.path.exists("../" + name):
            os.mkdir("../" + name)
        if not os.path.exists("../" + name + "/" + type):
            os.mkdir("../" + name + "/" + type)
        if flag:
            sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat", {"timeStamp_" + type : timeStamp, type: data})

    saveHashTable(table, "AppTable")

name = "Iron2"

type = "App"

path = "D:/SmartCampusData" + "/" + name + "/CPSLogger/" + type


fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for f in fileList :
    dateFile = f[-14:-4]
    # print(dateFile[5:7])
    if int(dateFile[5:7]) < 5 :
        continue
    print(dateFile)
    extractAndSave(name, type, dateFile)