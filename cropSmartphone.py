import importAGMS
import processingAppHistory
import processingMemory
import processingNotification
import processingCellLoc
import processingData
import processingPhone
import processingLocation
import processingWiFi
import os.path
import importEncodedData as iED
import appCategory
import numpy as np
import scipy.io as sio

directoryPath = "D:/ActionLocationDataset/"
# deviceID = "DDEE"

# date = "5_18"

day = {"2016_10_24" : 0, "2016_10_25" : 1, "2016_10_28" : 2}

startTime = {"geonho" : [[[9,12,0,0,], [11,12,0,0], [11,58,0,0], [13,0,0,0], [15,40,0,0], [17,0,0,0],[19,30,0,0],[23,55,0,0]],[[1,25,0,0],[9,30,0,0,],[12,50,0,0],[13,7,0,0],[14,30,0,0],[16,30,0,0],[17,53,0,0]]],
        "SG" : [[[11,13,0,0],[12,31,0,0,],[12,41,0,0],[13,49,0,0],[15,12,0,0],[15,31,0,0],[16,59,0,0],[17,5,0,0,],[18,13,0,0]], [[12,54,0,0],[14,14,0,0],[15,36,0,0]], [[10, 22, 0, 0], [10, 52, 0, 0, ], [11, 23, 0, 0], [11, 53, 0, 0], [12, 31, 0, 0], [13, 8, 0, 0]]],
        "HJ" : [[[14,23,11,412],[14,57,11,637],[15,32,37,391],[16,7,42,545],[17,48,27,995],[18,36,58,881],[18,48,53,532],[20,49,15,618],[21,38,54,85]], [[14,41,23,782],[15,10,52,539],[16,0,37,870],[17,45,49,970],[18,28,40,366],[18,40,12,620],[19,28,12,187]], [[10, 33, 30, 328], [11, 3, 19, 158], [11, 53, 14, 518], [12, 33, 9, 558]]]}
#
endTime = {"geonho" : [[[10,30,0,0,], [11,42,0,0], [12,56,0,0], [14,0,0,0], [16,40,0,0], [17,25,0,0],[20,30,0,0],[24,35,0,0]],[[1,55,0,0],[10,50,0,0,],[13,7,0,0],[13,54,0,0],[15,0,0,0],[17,20,0,0],[18,10,0,0]]],
        "SG" : [[[11,29,0,0],[12,37,0,0,],[13,35,0,0],[14,44,0,0],[15,24,0,0],[16,50,0,0],[17,4,0,0],[17,10,0,0,],[18,26,0,0]], [[13,5,0,0],[15,33,0,0],[17,47,0,0]], [[10,52,0,0],[11,23,0,0,],[11,42,0,0],[12,22,0,0],[12,55,0,0],[13,19,0,0]]],
        "HJ" : [[[14,57,11,637],[15,19,10,773],[16,7,42,545],[16,41,31,339],[17,57,45,482],[18,48,53,532],[19,13,51,185],[21,2,39,341],[23,12,20,438]], [[15,10,28,414],[16,0,37,870],[16,59,9,170],[18,16,6,91],[18,40,12,620],[19,11,44,282],[20,4,26,192]], [[10,53,2,682],[11,33,48,131],[12,22,39,620],[13,2,51,272]]]}


# startTime = {"SG": [[10, 22, 0, 0], [10, 52, 0, 0, ], [11, 23, 0, 0], [11, 53, 0, 0], [12, 31, 0, 0], [13, 8, 0, 0]],
#          "HJ": [[10, 33, 30, 328], [11, 3, 19, 158], [11, 53, 14, 518], [12, 33, 9, 558]]}
#
# endTime = {
#         "SG" : [[10,52,0,0],[11,23,0,0,],[11,42,0,0],[12,22,0,0],[12,55,0,0],[13,19,0,0]],
#         "HJ" : [[10,53,2,682],[11,33,48,131],[12,22,39,620],[13,2,51,272]]}


def change2Sec (time) :
    return time[0]*3600 + time[1]*60 + time[2]

def compareTime(time, start, end) :
    timeSec = change2Sec(time[0])
    startSec = change2Sec(start)
    endSec = change2Sec(end)
    if timeSec < startSec : #not start
        return 0
    elif timeSec < endSec :
        return 1
    else :
        return 2

def cropfile(name, type, date) :

    buffer = []

    startList = startTime[name]
    endList = endTime[name]

    iter = 0

    flag = False

    index = 0

    with open(directoryPath + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f :
        while True :
            line = f.readline()

            if not line : break
            if line[len(line) - 1] == ',': break
            if line[len(line) - 1] == '-': break
            if line[len(line) - 1] == '.': break

            dataF = line.split(",")

            time = [[float(timeChunk) for timeChunk in dataF[0:3]]]

            result = compareTime(time, startList[day[date]][iter], endList[day[date]][iter])

            index += 1

            if index == 10000 :
                print(index)

            if result == 0 :
                continue
            elif result == 1 :
                if not flag :
                    fileName = directoryPath + "result/" + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + "_" + str(iter) + ".txt"
                    writeFile = open(fileName , 'w')
                    flag = True
                writeFile.write(line)
                # buffer.append(line)

                # if len(buffer) == 10000:
                    # writeFile.write(buffer)
                    # buffer = []
            else :
                writeFile.close()
                iter += 1

                flag = False


nameList = ["geonho","SG", "HJ"]

phoneList = ["Iron2","GalaxyS6", "GalaxyS7"]

tableTemp = processingWiFi.loadHashTable("BSSID")
if tableTemp == "null" :
    table = dict()
else :
    table = tableTemp

for name in nameList :
    sio.savemat("../" + name + "/" + "timeTableAdd.mat", {"startTime" : startTime[name], "endTime" : endTime[name]})

# dateList = ["2016_10_24", "2016_10_25"]
#
# for name in nameList :
#     for date in dateList :
#         cropfile(name, "Acc", date)

for name in phoneList :
    print("AGM")

    path = directoryPath + name + "/CPSLogger/Acc"

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList :
        dateFile = f[-14:-4]
        importAGMS.extractAndSave(directoryPath, "Acc",name,dateFile,7)
        importAGMS.extractAndSave(directoryPath, "Gyro",name,dateFile,7)
        importAGMS.extractAndSave(directoryPath, "Mag",name,dateFile,7)

    type = "App"

    print(type)

    path = directoryPath + name + "/CPSLogger/" + type

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList:
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5:
            continue
        print(dateFile)
        processingAppHistory.extractAndSave(directoryPath, name, type, dateFile)
    path = directoryPath + "/" + name + "/CPSLogger/" + type
    print(name)

    type = "Mem"

    print(type)

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList:
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5:
            continue
        print(dateFile)
        processingMemory.extractAndSave(directoryPath, type, name, dateFile, 1)

    print("Noti")

    processingNotification.initCount(name)

    path = directoryPath + "/" + name + "/CPSLogger/Notification"
    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList:
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5:
            continue
        print(dateFile)
        processingNotification.extractAndSave(directoryPath, dateFile, name)

    type = "Signal"

    print(type)

    path = directoryPath + name + "/CPSLogger/" + type
    print(name)

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList :
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5 :
            continue
        print(dateFile)
        processingCellLoc.extractAndSave(directoryPath, name, type, dateFile)

    type = "Data"

    print(type)

    path = directoryPath + name + "/CPSLogger/" + type
    print(name)

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList :
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5 :
            continue
        print(dateFile)
        processingData.extractAndSave(directoryPath, name, type, dateFile)

    type = "Phone"
    print(type)

    path = directoryPath + name + "/CPSLogger/" + type

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList :
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5 :
            continue
        print(dateFile)
        processingPhone.extractAndSave(directoryPath, name, type, dateFile)

    type = "Location"
    print(type)

    path = directoryPath + name + "/CPSLogger/" + type

    fileLIst = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for file in fileLIst :
        dateFile = file[-14:-4]
        print(dateFile)
        processingLocation.extractAndSave(directoryPath, type, name, dateFile, 3)

    type = "Wifi"

    print(type)

    path = directoryPath + name + "/CPSLogger/" + type

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList:
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5:
            continue
        print(dateFile)
        timeStamp, data = iED.extract(directoryPath, name, type, dateFile, True)
        if len(data) == 0:
            continue
        temp = [processingWiFi.processingAP(dataF, table) for dataF in data]
        iED.saveTomat(type, dateFile, timeStamp, temp, name)

processingWiFi.saveHashTable(table, "BSSID")
processingAppHistory.saveCount(processingAppHistory.phoneList)
appCategory.saveTable()
processingNotification.saveCount(phoneList)