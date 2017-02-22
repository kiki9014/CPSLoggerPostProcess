# import subprocess
import processingData
import importAGMS
import processingNotification
import processingCellLoc
import processingAppHistory
import processingPhone
import processingWiFi
import processingMemory
import processingPower
import importEncodedData as iED
import appCategory

directoryPath = "D:/Data/"

# Participant list
phoneList = ["P1","P2","P3","P4","P5"]

# Load Wifi AP list
tableTemp = processingWiFi.loadHashTable("BSSID")
if tableTemp == "null" :
    table = dict()
else :
    table = tableTemp

# Date that processing is started
season4Date = "2017_01_01"

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

# Read date from pre-written file (dateList_Name.txt)
def getDateList(path, name) :
    list = []
    with open(path + "/" + name + "/" + "dateList_" + name + ".txt", 'r') as f :
        while True :
            line = f.readline().rstrip("\n")

            if not line : break

            list.append(line)

    return list

# Initialize app count
processingAppHistory.count = processingAppHistory.initAppProcessing(phoneList)

# Main part
for name in phoneList :
    print("Current User : " + name)
    print("AGM")

    dateList = getDateList(directoryPath, name) # Get List of date

    for dateFile in dateList :
        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        importAGMS.extractAndSave(directoryPath, "Acc",name,dateFile,7)
        importAGMS.extractAndSave(directoryPath, "Gyro",name,dateFile,7)
        importAGMS.extractAndSave(directoryPath, "Mag",name,dateFile,7)

    type = "App"

    print(type)

    for dateFile in dateList :
        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        processingAppHistory.extractAndSave(directoryPath, name, type, dateFile)

    type = "Mem"

    print(type)

    for dateFile in dateList :
        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        processingMemory.extractAndSave(directoryPath, type, name, dateFile, 1)

    print("Noti")

    processingNotification.initCount(name)

    for dateFile in dateList :
        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        processingNotification.extractAndSave(directoryPath, dateFile, name)

    type = "Signal"

    print(type)

    print(name)

    for dateFile in dateList :
        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        processingCellLoc.extractAndSave(directoryPath, name, type, dateFile)

    type = "Data"

    print(type)

    print(name)

    for dateFile in dateList :
        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        processingData.extractAndSave(directoryPath, name, type, dateFile)

    type = "Phone"
    print(type)

    for dateFile in dateList :
        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        processingPhone.extractAndSave(directoryPath, name, type, dateFile)

    type = "Location"
    print(type)

    type = "Wifi"

    print(type)

    for dateFile in dateList :
        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        timeStamp, data = iED.extract(directoryPath, name, type, dateFile, True)    # Read AP data from Wifi raw data
        if len(data) == 0:
            continue
        temp = [processingWiFi.processingAP(dataF, table) for dataF in data]        # Process WiFi AP data
        iED.saveTomat(type, dateFile, timeStamp, temp, name)                        # Save data

    type = 'Power'

    print(type)

    for dateFile in dateList :

        if checkSeason(dateFile, season4Date) == False :
            continue
        print(dateFile)
        processingPower.extractAndSave(directoryPath, type, name, dateFile)

# Save updated lists
processingWiFi.saveHashTable(table, "BSSID")
processingAppHistory.saveCount(phoneList)
appCategory.saveTable()
processingNotification.saveCount(phoneList)