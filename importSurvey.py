import numpy as np
import scipy.io as sio
import os.path
import sys

directoryPath = "D:/SmartCampusData/"

# deviceID = "DDEE"

def processingTime (str) :
    data = str.split("_")

    return [float(dataF) for dataF in data[2:]]

def processingItem(str, data) :
    # print(str)
    itemStr = str.split(":")
    # print(itemStr[1])

    # if itemStr[-1].isnumeric() :
    #     content = int(itemStr[-1])
    # else :
    #     content = (itemStr[-1].replace(" ", "")).encode('UTF-8', 'ignore')

    try :
        content = int(itemStr[-1])
    except ValueError :
        content = (itemStr[-1].replace(" ", "")).encode('UTF-8', 'ignore')

    data[itemStr[0]] = content

    return data

def processingData(str, data) :
    chunk = str.split(",")

    # data = [int(processingItem(dataF)) for dataF in chunk[-7:]]
    for dataF in chunk[-7:] :
        data = processingItem(dataF, data)

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

            print(survey)

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

deviceIDList = ["DDEE", "6DEB", "6D57", "C6EC", "6E11","6E23"]
for deviceID in deviceIDList :
    path = directoryPath + deviceID
    print(deviceID)
    dirList = [d for d in os.listdir(path) if not os.path.isfile(os.path.join(path, d))]
    for dir in dirList :
        date = dir
        print(date)
        extractAndSave(deviceID, date)