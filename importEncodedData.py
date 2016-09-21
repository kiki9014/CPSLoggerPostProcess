import base64
import numpy as np
import numpy.matlib as npmlib
import scipy.io as sio
import os.path

directoryPath = "D:/SmartCampusData"

def saveTomat(type,date,timeStamp, data, name) :
    if not os.path.exists("../" + name) :
        os.mkdir("../" + name)
    sio.savemat("../" + name +  "/" + type + "_" + date + ".mat", {"timeStamp_" + type + "_" + date : timeStamp, type + "_" + date : data})
    # sio.savemat(type + "Data_" + date + ".mat", {"timeStamp_" + type + "_" + date : timeStamp, type + "_" + date : data})

def extractAndSave(name, type, date, variable = False, size = 0) :
    timeStamp, data = extract(name, type, date, variable, size)
    saveTomat(type, date, timeStamp, data, name)

def extract(name, type, date, variable = False, size = 0) :
    data = [];
    with open(directoryPath+"/" + name + "/CPSLogger/" + type + "/CPSLogger_" + type + "_" + date + ".txt", 'r') as f :
        index = 0

        buffer = []
        flag = False

        while True :
            line = f.readline()
            if not line : break

            dataF = line.split(",")

            if variable :
                chunkSize = dataF[3]
            else :
                chunkSize = size

            if len(dataF) != chunkSize :
                if type != "Wifi" :
                    continue
            #
            # [True for dataChunk in dataF if len(dataChunk)%4 == 0]
            # if
            time = [[float(timeChunk) for timeChunk in dataF[0:3]]]
            decodeData =  [base64.b64decode(dataChunk).decode('UTF-8') for dataChunk in dataF[3:] if len(dataChunk)%4 == 0]
            # print(time)
            print(decodeData)

            if len(decodeData) < 3 :
                print(decodeData)

            if not flag :
                data = np.array(decodeData)
                # timeStamp = np.array(time)
                timeStamp = npmlib.repmat(time,len(decodeData),1)
                flag = True
            else :
                data = np.append(data,decodeData,axis=0)
                repTime = npmlib.repmat(time,len(decodeData),1)
                # print(repTime)
                timeStamp = np.append(timeStamp, repTime, axis=0)

        # sio.savemat(type + "Data_" + date + ".mat", {"timeStamp_" + type + "_" + date : timeStamp, type + "_" + date : data})
    if len(data) == 0 :
        return "null", data
    else : return timeStamp, data

# date = "2016_04_14"
#

# name = "Iron2"

# extractAndSave("Hist",date,False,5)
# extractAndSave(name, "Clip",date,False,5)
# ts, data = extract(name, "Clip", date, False, 5)
# print("data is " + data)
# extractAndSave("Book",date,False,5)
# extractAndSave("Key",date,False,5)
# extractAndSave("Wifi",date,True)