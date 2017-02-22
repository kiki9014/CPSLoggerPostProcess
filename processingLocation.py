import numpy as np
import scipy.io as sio
import os.path
import sys

directoryPath = "D:/SmartCampusData"

def dataArrange(line) :
    data = line.split(",")
    dataF = [float(datum) for datum in data]
    return dataF

def extractAndSave(path, type, name, date, size) :
    flag = False
    try :
        with open(path + "/" + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f :
            while True :
                line = f.readline().rstrip("\n")
                if not line : break
                if line[len(line)-1] == '-' : break
                if line[len(line)-1] == '.' : break

                dataF = line.split(",")

                if len(dataF) < 4 : break
                if "SAT" in dataF :
                    parsed = [0, 0, 0]
                else :
                    parsed = [float(datum) for datum in dataF[4:]]
                    if line[len(line)-1] == ',' : break
                time = [[float(datum) for datum in dataF[0:3]]]

                if len(parsed) != size :
                    continue


                if not flag:
                    data = np.array([parsed])
                    timeStamp = np.array(time)
                    flag = True
                else :
                    data = np.append(data, [parsed], axis=0)
                    timeStamp = np.append(timeStamp, time, axis=0)

    except IOError as error :
        print("Error occurred when processing Location : {0}".format(error))
    except:
        print("Unexpected error occurred : " + sys.exc_info()[0])
    if not flag :
        print("No location data")
        timeStamp = np.array([])
        data = np.array([])
        flag = True
    if not os.path.exists("../" + name) :
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + type) :
        os.mkdir("../" + name + "/" + type)
    if flag :
        sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat", {"timeStamp_" + type : timeStamp, type : data})
