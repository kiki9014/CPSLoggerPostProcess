import numpy as np
import scipy.io as sio
import os.path
import pickle
import sys

directoryPath = "D:/Data/" # Directory path to import raw survey data

radioValueDefault = {"down_1" : -1, "mod" : 0, "up_1" : 1, "undefined" : -99} # Used to label health and change of mood status

radioValueHealth = {"abs_un_healthy" : -1, "abs_mod_healthy" : 0, "abs_healthy" : 1, "undefined" : -99} # Used to label current health status, not change

radioValueActive = {"abs_un_active" : -1, "abs_mod_active" : 0, "abs_active" : 1, "undefined" : -99} # Used to label current activeness status, not change

radioValueHappy = {"abs_un_happy" : -1, "abs_mod_happy" : 0, "abs_happy" : 1, "undefined" : -99} # Used to label current happiness status, not change

# Dictionary to match proper mapping from survey item to label (radio button only)
radioValue = {"health" : radioValueDefault, "awakeness" : radioValueDefault, "happiness" : radioValueDefault, "currHealth" : radioValueHealth, "currActiveness" : radioValueActive, "currHappiness" : radioValueHappy}

# Default activity and location list
activityList = {"식사중" : 0, "컴퓨터사용중" : 1, "핸드폰사용중" : 2, "필기중" : 3, "걷는중" : 4, "엎드려자는중" : 5}
locationList = {"식당" : 0, "카페" : 1, "도서관"  : 2, "강의실" : 3, "연구실" : 4, "실험실" : 5, "기숙사" : 6}

defaultLabelList = {"location" : locationList, "activity" : activityList}

labelList = {}

# Date that data collection is started
season4Date = "1_01"

itemLength = [7, 7, 8, 11] # Length of item that participant replied season 1~3 in done with lab people, 4 is done with other people

# Read available date from pre-written file (dateList_Name.txt)
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

# Save updated list of label to pkl file
def saveLabelList(obj, tableName) :
    with open(tableName + ".pkl", 'wb') as f :
        pickle.dump(obj,f, pickle.DEFAULT_PROTOCOL)

# Label text data (location, activity) to number from list
def getLabelFromList(name, type) :
    changedName = (name.replace(" ", ""))
    typeList = labelList[type]
    if changedName in typeList :    # If the string is in the list, return matched value
        return typeList[changedName]
    else :  # If not, user input number and return the number
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

# Dictionary of functions that process survey item
season3Item = {"location" : getLabelFromList, "people" : processingNumber, "companion" : processingNumber, "activity" : getLabelFromList, "heartRate" : processingNumber, "health" : processingRadio, "awakeness" : processingRadio, "happiness" : processingRadio}

season4Item = {"location" : getLabelFromList, "people" : processingNumber, "companion" : processingNumber, "activity" : getLabelFromList, "heartRate" : processingNumber, "health" : processingRadio, "awakeness" : processingRadio, "happiness" : processingRadio, "currHealth" : processingRadio, "currActiveness" : processingRadio, "currHappiness" : processingRadio}

# Check date is right
def checkSeason(dateStr, seasonStr) :
    date = [int(dateChunk) for dateChunk in dateStr.split("_")]
    season = [int(seasonChunk) for seasonChunk in seasonStr.split("_")]

    if date[0] < season[0] :
        return False
    elif date[1] < season[1] :
        return False
    else :
        return True

# Change time to float array
def processingTime (str) :
    data = str.split("_")

    return [float(dataF) for dataF in data[2:]]

# Save raw text (location, activity)
def processingRaw(string, data) :
    itemStr = string.split(":")
    value = itemStr[-1].encode('UTF-8')

    data[itemStr[0] + "_Raw"] = value
    print(value)

    return data

def processingItem(str, data) :
    itemStr = str.split(":")

    content = season4Item[itemStr[0]](itemStr[-1],itemStr[0])

    data[itemStr[0]] = content

    return data

def processingData(str, data) :
    chunk = str.split(",")

    for dataF in chunk[-itemLength[3]:] :
        data = processingItem(dataF, data) # Processing survey item

    data = processingRaw(chunk[-itemLength[3]], data) # Add raw string of location to data
    data = processingRaw(chunk[-itemLength[3] + 3], data) # Add raw string of activity to data

    return data

def extractAndSave(name, date) :

    # Before season 2, response are stored without .txt extension
    if os.path.isfile(directoryPath + name + "/Gear/" + date + "/Survey_John") :
        fileName = "Survey_John"
    else :
        fileName = "Survey_John.txt"

    # Flag indicates file is empty. if file exist and has data, flag change to true
    flag = False
    try :
        with open(directoryPath + name + "/Gear/" + date + "/" + fileName,  "r", encoding="utf8") as f :    # Read survey file. file is automatically closed when it ends
            while True :
                line = f.readline().rstrip('\n')

                # If read line is incomplete (file is end), processing is end
                if not line : break
                line = line[:-1]
                if line[-1] == "," : line = line[:-1]

                # Split survey time and survey items, length is must 2
                fragment = line.split("\t")
                if len(fragment) < 2 :
                    print("Something is wrong in " + name + " when" + date)
                    break
                survey = {} # Empty space to save data

                time = processingTime(fragment[0])

                survey = processingData(fragment[-1], survey)

                survey["time"] = time # Merge time data and survey data

                if not flag :
                    data = np.array([survey])
                    flag = True
                else :
                    data = np.append(data, [survey], axis=0)
    except IOError as error : # Almost of IOError is due to no file or directory in path. Designed error handling
        print("Error occurred when processing survey : {0}".format(error))
    except : # If below text is showed, we have problem
        print("Unexpected error occurred  : {0}".format(sys.exc_info()[0]))

    if not os.path.exists("../" + name):
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + date):
        os.mkdir("../" + name + "/" + date)
    if not flag :
        data = np.array([]) # Save empty matrix if survey file does not exist
    if flag :
        sio.savemat("../" + name + "/Survey_" + date + ".mat", {"Survey": data})

# Start part. Load list of label
loadedTable = loadHashTable("surveyLabelList")

if loadedTable == "null" :
    labelList = defaultLabelList
else :
    labelList = loadedTable

# List of participant
deviceIDList = ["P1","P2","P3","P4","P5"]

# Main part
for deviceID in deviceIDList :
    print(deviceID)
    dirList = getDateList(directoryPath, deviceID) # YYYY_MM_DD. In survey, M_DD is used (please change this part)
    for dir in dirList :
        date = dir[-4:] # Extract M_DD
        print(date)
        if checkSeason(date, season4Date) == False :
            continue
        print(date)
        extractAndSave(deviceID, date)

# Last part. Save updated list
saveLabelList(labelList, "surveyLabelList")

# print list
print(labelList["location"])
print(labelList["activity"])