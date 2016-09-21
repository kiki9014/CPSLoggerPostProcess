import numpy as np
import scipy.io as sio
import os.path

directoryPath = "D:/SmartCampusData"

def dataArrange(line) :
    data = line.split(",")
    dataF = [float(datum) for datum in data]
    return dataF

def extractAndSave(type, name, date, size) :
    with open(directoryPath + "/" + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f :
        flag = False
        while True :
            line = f.readline()
            if not line : break
            if line[len(line)-1] == ',' : break
            if line[len(line)-1] == '-' : break
            if line[len(line)-1] == '.' : break

            dataF = line.split(",")
            # print(dataF)

            if len(dataF) < 4 : break
            if dataF[3] == "SAT" : continue
            parsed = [float(datum) for datum in dataF[4:]]
            time = [[float(datum) for datum in dataF[0:3]]]

            if len(parsed) != size:
                continue


            if not flag:
                data = np.array([parsed])
                timeStamp = np.array(time)
                flag = True
            else :
                data = np.append(data, [parsed], axis=0)
                timeStamp = np.append(timeStamp, time, axis=0)

        # print("Complete")
        if not flag :
            print("No location data")
            return
        if not os.path.exists("../" + name) :
            os.mkdir("../" + name)
        sio.savemat("../" + name +  "/" + type + "_" + date + ".mat", {"timeStamp_" + type + "_" + date : timeStamp, type + "_" + date : data})

dateFile = "2016_05_18"

name = "Iron2"

type = "Location"

path = "D:/SmartCampusData" + "/" + name + "/CPSLogger/" + type

fileLIst = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

for file in fileLIst :
    dateFile = file[-14:-4]
    print(dateFile)
    extractAndSave(type, name, dateFile, 3)