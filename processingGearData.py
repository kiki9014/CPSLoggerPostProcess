import numpy as np
import scipy.io as sio
import os.path

directoryPath = "D:/SmartCampusData/"

# directoryPath = "D:/ActionLocationDataset/"
# deviceID = "DDEE"

# date = "5_18"

dataTypes = ["None", "gearAcc", "gearGyro", "gearMag", "gearUV", "gearLight", "gearPress", "gearHR", "gearBattery", "gearMemory"]
lenData = [0, 8, 8, 8, 6, 6, 6, 6, 6, 6]

def transGearToMat(name, date) :
    path = directoryPath + "/" + name + "/" + date

    fileDir = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[0:9] == "HWsensing"]

    data = {}
    buffer = {}

    for type in dataTypes:
        data[type] = []
        buffer[type] = []

    flags = [False for type in dataTypes]

    for file in fileDir :
        with open(directoryPath + "/" + name + "/" + date + "/" + file) as f:
            index = 0
            while True:
                line = f.readline()

                if not line : break
                if line[len(line)-1] == "-" : break
                if line[len(line)-1] == ',' : break
                if line[len(line)-1] == '.' : break

                dataF = line.split(",")

                if len(dataF) < 5 : break

                if len(dataF) < lenData[int(dataF[4])] : break

                time = [float(timeChunk) for timeChunk in dataF[0:4]]

                if index == 2603 :
                    print('Time')

                time[2] = time[2] + time[3]/1000

                del time[3]

                dataTypeNum = int(dataF[4])

                dataFragments = [float(dataFrag) for dataFrag in dataF[5:]]

                time.extend(dataFragments)

                dataChunk = time

                dataType = dataTypes[dataTypeNum]

                buffer[dataType].append(dataChunk)

                flag = flags[dataTypeNum]

                if len(buffer[dataType]) == 100000 :
                    # print(dataType)
                    if not flag :
                        data[dataType] = np.array(buffer[dataType])
                        flags[dataTypeNum] = True
                    else :
                        data[dataType] = np.append(data[dataType], buffer[dataType], axis=0)
                    buffer[dataType] = []

                index += 1
                if index%100000 == 0:
                    print(index)

    for dataType in dataTypes :
        if not flags[dataTypes.index(dataType)]:
            data[dataType] = np.array(buffer[dataType])
        else:
            data[dataType] = np.append(data[dataType], buffer[dataType], axis=0)

    del data["None"]

    if not os.path.exists("../" + name):
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + date) :
        os.mkdir("../" + name + "/" + date)
    sio.savemat("../" + name + "/" + date + "/" + "gearSensing_" + date + ".mat", data)

deviceIDList = ["DDEE", "6DEB", "6D57", "C6EC", "6E11","6E23"]
for deviceID in deviceIDList :
    path = directoryPath + deviceID
    print(deviceID)
    dirList = [d for d in os.listdir(path) if not os.path.isfile(os.path.join(path, d))]
    for dir in dirList :
        date = dir
        print(date)
        transGearToMat(deviceID, date)