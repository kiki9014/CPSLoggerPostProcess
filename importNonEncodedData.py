import base64
import numpy as np
import scipy.io as sio

directoryPath = "D:/CPSLogger"

def extractAndSave(type, name, variable = False, size = 0) :
    try :
        with open(directoryPath+"/" + type + "/" + "CPSLogger_" + type + "_" + name + ".txt",'r') as f :
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
                content = dataF[4:]

                print(time)
                print(content)

                if not flag :
                    data = np.array(content)
                    timeStamp = np.array(time)
                    flag = True
                else :
                    data = np.append(data,content,axis=0)
                    timeStamp = np.append(timeStamp, time,axis=0)
    except IOError as error :
        print("Error occurred when processing iNED : {0}".format(error))
    sio.savemat(type + "Data_" + name + ".mat", {"timeStamp_" + type + "_" + name : timeStamp, type + "_" + name : data})