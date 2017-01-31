# import subprocess
import processingData
import importAGMS
# import importSurvey
import processingNotification
import processingCellLoc
import processingAppHistory
import processingPhone
import processingWiFi
import processingLocation
import processingMemory
import processingPower
import os.path
import importEncodedData as iED
import appCategory

#
# exec("processingData")
# exec("importAGMS")
# exec("importSurvey")
# exec("processingCellLoc")
# exec("processingAppHistory")
# exec("processingPhone")
# exec("processingNotification")

directoryPath = "D:/Data/"

# phoneList = ["Iron2", "GalaxyS6", "GalaxyS7", "Vu2", "G5", "Nexus5X"]
phoneList = ["P3", "P4"]

completeList = ["Iron2"]

tableTemp = processingWiFi.loadHashTable("BSSID")
if tableTemp == "null" :
    table = dict()
else :
    table = tableTemp

# dateList = ["2016_10_24", "2016_10_25"]
#
# for name in nameList :
#     for date in dateList :
#         cropfile(name, "Acc", date)

season3Date = "2016_11_01"

def checkSeason(dateStr, seasonStr) :
    date = [int(dateChunk) for dateChunk in dateStr.split("_")]
    season = [int(seasonChunk) for seasonChunk in seasonStr.split("_")]

    if date[0] < season[0] :
        return False
    elif date[0] > season[0] :
        return True
    elif date[1] < season[1] :
        return False
    elif date[2] < season[2] :
        return False
    else :
        return True

for name in phoneList :
    # if name in completeList :
    #     continue
    print("Current User : " + name)
    print("AGM")

    path = directoryPath + name + "/CPSLogger/Acc"

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList :
        dateFile = f[-14:-4]
        if checkSeason(dateFile, season3Date) == False :
            continue
        print(dateFile)
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
        # if int(dateFile[5:7]) < 5:
        #     continue
        if checkSeason(dateFile,season3Date) == False :
            continue
        print(dateFile)
        processingAppHistory.extractAndSave(directoryPath, name, type, dateFile)
    path = directoryPath + "/" + name + "/CPSLogger/" + type

    type = "Mem"

    print(type)

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList:
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if checkSeason(dateFile,season3Date) == False :
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
        if checkSeason(dateFile,season3Date) == False :
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
        if checkSeason(dateFile,season3Date) == False :
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
        if checkSeason(dateFile,season3Date) == False :
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
        if checkSeason(dateFile,season3Date) == False :
            continue
        print(dateFile)
        processingPhone.extractAndSave(directoryPath, name, type, dateFile)

    type = "Location"
    print(type)

    path = directoryPath + name + "/CPSLogger/" + type

    fileLIst = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for file in fileLIst :
        dateFile = file[-14:-4]
        if checkSeason(dateFile,season3Date) == False :
            continue
        print(dateFile)
        processingLocation.extractAndSave(directoryPath, type, name, dateFile, 3)

    type = "Wifi"

    print(type)

    path = directoryPath + name + "/CPSLogger/" + type

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList:
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if checkSeason(dateFile,season3Date) == False :
            continue
        print(dateFile)
        timeStamp, data = iED.extract(directoryPath, name, type, dateFile, True)
        if len(data) == 0:
            continue
        temp = [processingWiFi.processingAP(dataF, table) for dataF in data]
        iED.saveTomat(type, dateFile, timeStamp, temp, name)

    type = 'Power'

    print(type)

    path = directoryPath + name + "/CPSLogger/" + type

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList:
        dateFile = f[-14:-4]

        if checkSeason(dateFile, season3Date) == False :
            continue
        print(dateFile)
        processingPower.extractAndSave(directoryPath, type, name, dateFile)

processingWiFi.saveHashTable(table, "BSSID")
processingAppHistory.saveCount(processingAppHistory.phoneList)
appCategory.saveTable()
processingNotification.saveCount(phoneList)