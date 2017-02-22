import os.path
import numpy as np
import scipy.io as sio
import sys

directoryPath = "D:/SmartCampusData/"

powerTypes = ["battery", "screen", "headphone"]
length = [5, 1, 1]

def parsingBoolAndNumber (data) :
    if data.isnumeric() or "." in data:
        return float(data)
    else :
        dataC = data[0].upper() + data[1:]
        return int(dataC == "True")

def processingPower(type, dataStr) :
    if type == "battery" :
        data = [parsingBoolAndNumber(dataChunk) for dataChunk in dataStr]
    elif type == "screen" :
        data = [parsingBoolAndNumber(dataChunk) for dataChunk in dataStr]
    else :
        data = []
    return data

def extractAndSave (path, type, name, date) :

    data = {}

    for types in powerTypes:
        data[types] = []

    flags = [False for temp in powerTypes]

    try :
        with open(path + "/" + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f :

            while True :
                line = f.readline().rstrip('\n')

                if not line: break
                if line[len(line) - 1] == ',': break
                if line[len(line) - 1] == '-': break
                if line[len(line) - 1] == '.': break

                dataF = line.split(",")

                time = [float(timeChunk) for timeChunk in dataF[0:3]]

                dataType = powerTypes.index(dataF[3])

                parsed = processingPower(powerTypes[dataType],dataF[4:])
                if len(parsed) != length[dataType] : continue
                # print(parsed)

                time.extend(parsed)

                dataChunk = time

                if not flags[dataType]:
                    data[powerTypes[dataType]] = np.array([dataChunk])
                    flags[dataType] = True
                else:
                    data[powerTypes[dataType]] = np.append(data[powerTypes[dataType]], [dataChunk], axis=0)
    except IOError as error :
        print("Error occurred when processing power : {0}".format(error))
    except :
        print("Unexpected error occurred : " + sys.exc_info()[0])

    for dataType in powerTypes :
        idxData = powerTypes.index(dataType)
        if not os.path.exists("../" + name):
            os.mkdir("../" + name)
        if not os.path.exists("../" + name + "/" + type):
            os.mkdir("../" + name + "/" + type)
        if not flags[idxData] :
            flags[idxData] = True
            data[dataType] = np.array([])
        if flags[idxData]:
            sio.savemat("../" + name + "/" + type + "/" + dataType + "_" + date + ".mat", {dataType: data[dataType]})
