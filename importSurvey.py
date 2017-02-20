import numpy as np
import scipy.io as sio
import os.path
import pickle
import sys
import sys

directoryPath = "D:/Data/"

# deviceID = "DDEE"

radioValueDefault = {"down_1" : -1, "mod" : 0, "up_1" : 1, "undefined" : -99}

radioValueHealth = {"abs_un_healthy" : -1, "abs_mod_healthy" : 0, "abs_healthy" : 1, "undefined" : -99}

radioValueActive = {"abs_un_active" : -1, "abs_mod_active" : 0, "abs_active" : 1, "undefined" : -99}

radioValueHappy = {"abs_un_happy" : -1, "abs_mod_happy" : 0, "abs_happy" : 1, "undefined" : -99}

radioValue = {"health" : radioValueDefault, "awakeness" : radioValueDefault, "happiness" : radioValueDefault, "currHealth" : radioValueHealth, "currActiveness" : radioValueActive, "currHappiness" : radioValueHappy}

activityList = {"식사중" : 0, "컴퓨터사용중" : 1, "핸드폰사용중" : 2, "필기중" : 3, "걷는중" : 4, "엎드려자는중" : 5}
locationList = {"식당" : 0, "카페" : 1, "도서관"  : 2, "강의실" : 3, "연구실" : 4, "실험실" : 5, "기숙사" : 6}

defaultLabelList = {"location" : locationList, "activity" : activityList}

labelList = {}

season3Date = "1_01"

itemLength = [7, 7, 11]

def getDateList(path, name) :
    list = []
    with open(path + "/" + name + "/" + "dateList_" + name + ".txt", 'r') as f :
        while True :
            line = f.readline().rstrip("\n")

            if not line : break

            list.append(line)

    return list

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
        return radioValue[type][item]

def processingNumber(item, type) :
    if item == "+":
        return 99
    return int(item)

season3Item = {"location" : getLabelFromList, "people" : processingNumber, "companion" : processingNumber, "activity" : getLabelFromList, "heartRate" : processingNumber, "health" : processingRadio, "awakeness" : processingRadio, "happiness" : processingRadio}

season4Item = {"location" : getLabelFromList, "people" : processingNumber, "companion" : processingNumber, "activity" : getLabelFromList, "heartRate" : processingNumber, "health" : processingRadio, "awakeness" : processingRadio, "happiness" : processingRadio, "currHealth" : processingRadio, "currActiveness" : processingRadio, "currHappiness" : processingRadio}

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

    content = season4Item[itemStr[0]](itemStr[-1],itemStr[0])

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
    if os.path.isfile(directoryPath + name + "/Gear/" + date + "/Survey_John") :
        fileName = "Survey_John"
    else :
        fileName = "Survey_John.txt"

    # print(directoryPath + name + "/Gear/" + date + "/Survey_John")
    flag = False
    try :
        with open(directoryPath + name + "/Gear/" + date + "/" + fileName,  "r", encoding="utf8") as f :
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
    except IOError as error :
        print("Error occurred when processing survey : {0}".format(error))
    except :
        print("Unexpected error occurred  : {0}".format(sys.exc_info()[0]))

    if not os.path.exists("../" + name):
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + date):
        os.mkdir("../" + name + "/" + date)
    if not flag :
        data = np.array([])
    if flag :
        sio.savemat("../" + name + "/Survey_" + date + ".mat", {"Survey": data})
            # sio.loadmat("../" + name + "/Survey_" + date + ".mat")

# sys.setdefaultencoding()

loadedTable = loadHashTable("surveyLabelList")

if loadedTable == "null" :
    labelList = defaultLabelList
else :
    labelList = loadedTable

# deviceIDList = ["DDEE", "6DEB", "6D57", "C6EC", "6E11", "6E23"]
# deviceIDList = ["6DEB"]
deviceIDList = ["P1","P2","P3","P4","P5"]

for deviceID in deviceIDList :
    path = directoryPath + deviceID
    print(deviceID)
    dirList = getDateList(directoryPath, deviceID)
    # dirList = [d for d in os.listdir(path) if not os.path.isfile(os.path.join(path, d))]
    for dir in dirList :
        date = dir[-4:]
        print(date)
        if checkSeason(date, season3Date) == False :
            continue
        print(date)
        extractAndSave(deviceID, date)

saveLabelList(labelList, "surveyLabelList")