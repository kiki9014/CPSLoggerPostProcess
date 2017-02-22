import base64
import numpy as np
import numpy.matlib as npmlib
import scipy.io as sio
import os.path
import sys

directoryPath = "D:/SmartCampusData"

def saveTomat(type,date,timeStamp, data, name) :
    if not os.path.exists("../" + name) :
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + type) :
        os.mkdir("../" + name + "/" + type)
    sio.savemat("../" + name +  "/" +  type + "/" + type + "_" + date + ".mat", {"timeStamp_" + type  : timeStamp, type : data})

def extractAndSave(name, type, date, variable = False, size = 0) :
    timeStamp, data = extract(name, type, date, variable, size)
    saveTomat(type, date, timeStamp, data, name)

def extract(path, name, type, date, variable = False, size = 0) :
    data = []
    timeStamp = []
    try :
        with open(path+"/" + name + "/CPSLogger/" + type + "/CPSLogger_" + type + "_" + date + ".txt", 'r') as f :
            flag = False

            while True :
                line = f.readline().rstrip('\n')
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
                try :
                    if type == "Wifi" :
                        decodeData =  [base64.b64decode(dataChunk).decode('UTF-8') for dataChunk in dataF[3:] if len(dataChunk)%4 == 0]
                    else :
                        decodeData =  [base64.b64decode(dataChunk).decode('UTF-8') for dataChunk in dataF[4:] if len(dataChunk)%4 == 0]
                except UnicodeDecodeError :
                    print("unicodeError occurred")
                    continue

                if not flag :
                    data = np.array(decodeData)
                    timeStamp = npmlib.repmat(time,len(decodeData),1)
                    flag = True
                else :
                    data = np.append(data,decodeData,axis=0)
                    repTime = npmlib.repmat(time,len(decodeData),1)
                    timeStamp = np.append(timeStamp, repTime, axis=0)

    except IOError as error:
        print("Error occurred when processing iED : {0}".format(error))
    except :
        print("Unexpected error occurred : " + sys.exc_info()[0])
    return  timeStamp, data