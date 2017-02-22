import numpy as np
import scipy.io as sio
import os.path
import pickle
import sys

directoryPath = "D:/SmartCampusData"

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

def processingPhoneNumber(string, table) :
    number = ''.join(x for x in string if x.isdigit())

    if number == '' :
        return "null"
    else :
        return hashing(number, table)

def extractAndSave(path, name, type, date) :
    tableTemp = loadHashTable("PhoneNumber")
    if tableTemp == "null" :
        table = dict()
    else :
        table = tableTemp
    flag = False

    try :
        with open(path + "/" + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f:

            while True :
                line = f.readline().rstrip('\n')

                if not line: break
                if line[len(line) - 1] == ',': break
                if line[len(line) - 1] == '-': break
                if line[len(line) - 1] == '.': break

                dataF = line.split(",")

                time = [[float(timeChunk) for timeChunk in dataF[0:3]]]

                parsed = processingPhoneNumber(dataF[-1], table)
                if parsed == "null" :
                    continue

                if not flag :
                    data = np.array(parsed)
                    timeStamp = np.array(time)
                    flag = True
                else :
                    data = np.append(data, parsed)
                    timeStamp = np.append(timeStamp, time, axis=0)
    except IOError as error :
        print("Error occurred when processing phone : {0}".format(error))
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
    if flag:
        sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat",{"timeStamp_" + type: timeStamp, type: data})

    saveHashTable(table, "PhoneNumber")