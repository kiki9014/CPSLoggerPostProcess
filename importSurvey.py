import numpy as np
import scipy.io as sio
import os.path
import pickle
import sys

directoryPath = "D:/SmartCampusData/"

# deviceID = "DDEE"

radioValue = {"down_1" : -1, "mod" : 0, "up_1" : 1}

activityList = {"식사중" : 0, "컴퓨터사용중" : 1, "핸드폰사용중" : 2, "필기중" : 3, "걷는중" : 4, "엎드려자는중" : 5}
locationList = {"식당" : 0, "카페" : 1, "도서관"  : 2, "강의실" : 3, "연구실" : 4, "실험실" : 5, "기숙사" : 6}

defaultLabelList = {"location" : locationList, "activity" : activityList}

labelList = {}

season3Date = "11_1"

itemLength = [7, 7, 8]

def loadHashTable(tableName) :
    if not os.path.isfile(tableName + ".pkl") :
        return "null"
    with open(tableName + ".pkl", 'rb') as f :
        return pickle.load(f)

def saveLabelList(obj, tableName) :
    with open(tableName + ".pkl", 'wb') as f :
        pickle.dump(obj,f, pickle.DEFAULT_PROTOCOL)

def getLabelFromList(name, type) :
    changedName = (name.replace(" ", ""))
    typeList = labelList[type]
    if changedName in typeList :
        return typeList[changedName]
    else :
        print(typeList)
        number = input("Enter label index from above list or new one : %s" % changedName)
        number = int(number)
        typeList[changedName] = number
        return number

def processingRadio(item, type) :
    if item.isnumeric() :
        return int(item)
    else :
        return radioValue[item]

def processingNumber(item, type) :
    return int(item)

season3Item = {"location" : getLabelFromList, "people" : processingNumber, "companion" : processingNumber, "activity" : getLabelFromList, "heartRate" : processingNumber, "health" : processingRadio, "awakeness" : processingRadio, "happiness" : processingRadio}

def checkSeason(dateStr, seasonStr) :
    date = [int(dateChunk) for dateChunk in dateStr.split("_")]
    season = [int(seasonChunk) for seasonChunk in seasonStr.split("_")]

    if date[0] < season[0] :
        return False
    elif date[1] < season[1] :
        return False
    else :
        return True

def processingTime (str) :
    data = str.split("_")

    return [float(dataF) for dataF in data[2:]]

def processingRaw(string, data) :
    itemStr = string.split(":")
    value = itemStr[-1].encode('UTF-8')
    length = len(itemStr[-1])

    data[itemStr[0] + "_Raw"] = value
    # print(value.decode('UTF-8'))# + str(len(itemStr[-1])))
    print(value)# + str(len(itemStr[-1])))

    return data

def processingItem(str, data) :
    # print(str)
    itemStr = str.split(":")
    # print(itemStr[1])

    # if itemStr[-1].isnumeric() :
    #     content = int(itemStr[-1])
    # else :
    #     content = (itemStr[-1].replace(" ", "")).encode('UTF-8', 'ignore')

    content = season3Item[itemStr[0]](itemStr[-1],itemStr[0])

    # try :
    #     content = int(itemStr[-1])
    # except ValueError :
    #     content = (itemStr[-1].replace(" ", "")).encode('UTF-8', 'ignore')

    data[itemStr[0]] = content

    return data

def processingData(str, data) :
    chunk = str.split(",")

    # data = [int(processingItem(dataF)) for dataF in chunk[-7:]]
    for dataF in chunk[-itemLength[2]:] :
        data = processingItem(dataF, data)

    data = processingRaw(chunk[-itemLength[2]], data)
    data = processingRaw(chunk[-itemLength[2] + 3], data)

    return data

def extractAndSave(name, date) :
    if os.path.isfile(directoryPath + name + "/" + date + "/Survey_John") :
        fileName = "Survey_John"
    else :
        fileName = "Survey_John.txt"

    with open(directoryPath + name + "/" + date + "/" + fileName,  "r", encoding="utf8") as f :
        flag  = False
        while True :
            line = f.readline()
            if not line : break
            line = line[:-1]
            if line[-1] == "," : line = line[:-1]

            fragment = line.split("\t")
            if len(fragment) < 2 :
                print("Something is wrong in " + name + " when" + date)
                break
            survey = {}

            time = processingTime(fragment[0])

            survey = processingData(fragment[-1], survey)

            # survey = np.array(time)
            # survey = np.append(survey, item)

            dt = [("location", np.str_), ("awakeness", 'i8'), ("happiness", 'i8'), ("time", 'f8'), ("activity", np.str_), ("companion", 'i8'), ("heartRate", 'i8'), ("health", 'i8')]

            survey["time"] = time

            # print(survey)

            if not flag :
                data = np.array([survey])
                flag = True
            else :
                data = np.append(data, [survey], axis=0)

        if not os.path.exists("../" + name):
            os.mkdir("../" + name)
        if not os.path.exists("../" + name + "/" + date):
            os.mkdir("../" + name + "/" + date)
        if flag :
            sio.savemat("../" + name + "/Survey_" + date + ".mat", {"Survey": data})
            # sio.loadmat("../" + name + "/Survey_" + date + ".mat")

# sys.setdefaultencoding()

loadedTable = loadHashTable("surveyLabelList")

if loadedTable == "null" :
    labelList = defaultLabelList
else :
    labelList = loadedTable

deviceIDList = ["DDEE", "6DEB", "6D57", "C6EC", "6E11", "6E23"]
# deviceIDList = ["6DEB"]
for deviceID in deviceIDList :
    path = directoryPath + deviceID
    print(deviceID)
    dirList = [d for d in os.listdir(path) if not os.path.isfile(os.path.join(path, d))]
    for dir in dirList :
        date = dir
        if checkSeason(date, season3Date) == False :
            continue
        print(date)
        extractAndSave(deviceID, date)

saveLabelList(labelList, "surveyLabelList")