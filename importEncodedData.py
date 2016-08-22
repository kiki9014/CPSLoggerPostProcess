import base64
import numpy as np
import scipy.io as sio

directoryPath = "D:/CPSLogger"

def extractAndSave(type, name, variable = False, size = 0) :
    with open(directoryPath+"/" + type + "/" + "CPSLogger_" + type + "_" + name + ".txt",'r') as f :
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

            time = [[float(timeChunk) for timeChunk in dataF[0:3]]]
            decodeData =  [base64.b64decode(dataChunk).decode('UTF-8') for dataChunk in dataF[4:]]
            print(time)
            print(decodeData)

            if not flag :
                data = np.array(decodeData)
                timeStamp = np.array(time)
                flag = True
            else :
                data = np.append(data,decodeData,axis=0)
                timeStamp = np.append(timeStamp, time,axis=0)

        sio.savemat(type + "Data_" + name + ".mat", {"timeStamp_" + type + "_" + name : timeStamp, type + "_" + name : data})

# date = "2016_04_14"
#
# extractAndSave("Hist",date,False,5)
# extractAndSave("Clip",date,False,5)
# extractAndSave("Book",date,False,5)
# extractAndSave("Key",date,False,5)
# extractAndSave("Wifi",date,True)