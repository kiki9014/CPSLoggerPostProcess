import numpy as np
import scipy.io as sio
import os.path

# directoryPath = "D:/SmartCampusData/"

directoryPath = "D:/ActionLocationDataset/"
# deviceID = "DDEE"

# date = "5_18"

dataTypes = ["None", "gearAcc", "gearGyro", "gearMag", "gearUV", "gearLight", "gearPress", "gearHR", "gearBattery", "gearMemory"]
lenData = [0, 8, 8, 8, 6, 6, 6, 6, 6, 6]

day = {"10_24" : 0, "10_25" : 1}

start = {"geonho" : [[[9,12,0,0,], [11,12,0,0], [11,58,0,0], [13,0,0,0], [15,40,0,0], [17,0,0,0],[19,30,0,0],[23,55,0,0]],[[1,25,0,0],[9,30,0,0,],[12,50,0,0],[13,7,0,0],[14,30,0,0],[16,30,0,0],[17,53,0,0]]],
        "SG" : [[[11,13,0,0],[12,31,0,0,],[12,41,0,0],[13,49,0,0],[15,12,0,0],[15,31,0,0],[16,59,0,0],[17,5,0,0,],[18,13,0,0]], [[12,54,0,0],[14,14,0,0],[15,36,0,0]]],
        "HJ" : [[[14,23,11,412],[14,57,11,637],[15,32,37,391],[16,7,42,545],[17,48,27,995],[18,36,58,881],[18,48,53,532],[20,49,15,618],[21,38,54,85]], [[14,41,23,782],[15,10,52,539],[16,0,37,870],[17,45,49,970],[18,28,40,366],[18,40,12,620],[19,28,12,187]]]}

end = {"geonho" : [[[10,30,0,0,], [11,42,0,0], [12,56,0,0], [14,0,0,0], [16,40,0,0], [17,25,0,0],[20,30,0,0],[24,35,0,0]],[[1,55,0,0],[10,50,0,0,],[13,7,0,0],[13,54,0,0],[15,0,0,0],[17,20,0,0],[18,10,0,0]]],
        "SG" : [[[11,29,0,0],[12,37,0,0,],[13,35,0,0],[14,44,0,0],[15,24,0,0],[16,50,0,0],[17,4,0,0],[17,10,0,0,],[18,26,0,0]], [[13,5,0,0],[15,33,0,0],[17,47,0,0]]],
        "HJ" : [[[14,57,11,637],[15,19,10,773],[16,7,42,545],[16,41,31,339],[17,57,45,482],[18,48,53,532],[19,13,51,185],[21,2,39,341],[23,12,20,438]], [[15,10,28,414],[16,0,37,870],[16,59,9,170],[18,16,6,91],[18,40,12,620],[19,11,44,282],[20,4,26,192]]]}

def change2Sec (time) :
    return time[0]*3600 + time[1]*60 + time[2]

def compareTime(time, start, end) :
    timeSec = change2Sec(time)
    startSec = change2Sec(start)
    endSec = change2Sec(end)
    if timeSec < startSec : #not start
        return 0
    elif timeSec < endSec :
        return 1
    else :
        return 2

def saveBuffer(name, date, iter, buffer, data) :

    flags = [False for type in dataTypes]

    for dataType in dataTypes :
        if not flags[dataTypes.index(dataType)]:
            data[dataType] = np.array(buffer[dataType])
        else:
            data[dataType] = np.append(data[dataType], buffer[dataType], axis=0)

    del data["None"]

    number = str(iter)

    if not os.path.exists("../" + name):
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + date) :
        os.mkdir("../" + name + "/" + date)
    if not os.path.exists("../" + name + "/" + date + "/" + number) :
        os.mkdir("../" + name + "/" + date + "/" + number)
    sio.savemat("../" + name + "/" + date + "/" + number + "/" + "gearSensing_" + date + ".mat", data)

def resetData() :
    data = {}
    buffer = {}
    for type in dataTypes:
        data[type] = []
        buffer[type] = []

    return data, buffer

def transGearToMat(name, date) :
    path = directoryPath + "/" + name + "/Gear/" + date

    fileDir = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[0:9] == "HWsensing"]
    #
    # data = {}
    # buffer = {}

    startList = start[name]
    endList = end[name]

    iter = 0

    data, buffer = resetData()

    flags = [False for type in dataTypes]

    for file in fileDir :
        with open(path + "/" + file) as f:
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

                time[2] = time[2] + time[3]/1000

                del time[3]

                index += 1
                if index%100000 == 0:
                    print(index)
                if iter == len(startList[day[date]]) :
                    break
                result = compareTime(time, startList[day[date]][iter], endList[day[date]][iter])

                if result == 0 :
                    continue
                elif result == 1 :
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
                else :
                    saveBuffer(name, date, iter, buffer, data)
                    iter += 1
                    data, buffer = resetData()

                    flags = [False for type in dataTypes]

deviceIDList = ["geonho", "SG", "HJ"]
for deviceID in deviceIDList :
    path = directoryPath + deviceID + "/Gear"
    print(deviceID)
    dirList = [d for d in os.listdir(path) if not os.path.isfile(os.path.join(path, d))]
    for dir in dirList :
        date = dir
        print(date)
        transGearToMat(deviceID, date)