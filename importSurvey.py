import numpy as np
import scipy.io as sio
import os.path

directoryPath = "D:/SmartCampusData/"

# deviceID = "DDEE"

def processingTime (str) :
    data = str.split("_")

    return [float(dataF) for dataF in data[2:]]

def processingItem(str) :
    # print(str)
    itemStr = str.split(":")
    # print(itemStr[1])

    if itemStr[1].isnumeric() :
        return itemStr[1]
    else :
        return 0

def processingData(str) :
    chunk = str.split(",")

    data = [int(processingItem(dataF)) for dataF in chunk[-6:]]

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
            if len(fragment) != 2 :
                print("Somethins is wrong in " + name + " when" + date)
                break

            time = processingTime(fragment[0])

            item = processingData(fragment[1])

            survey = np.array(time)
            survey = np.append(survey, item)

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

deviceIDList = ["DDEE", "6DEB", "6D57", "C6EC", "6E11","6E23"]
for deviceID in deviceIDList :
    path = directoryPath + deviceID
    print(deviceID)
    dirList = [d for d in os.listdir(path) if not os.path.isfile(os.path.join(path, d))]
    for dir in dirList :
        date = dir
        print(date)
        extractAndSave(deviceID, date)