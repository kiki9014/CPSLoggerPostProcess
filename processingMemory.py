import numpy as np
import scipy.io as sio
import os.path

directoryPath = "D:/SmartCampusData"

def dataArrange(line) :
    data = line.split(",")
    dataF = [float(datum) for datum in data]
    return dataF

def extractAndSave(path, type, name, date, size) :
    with open(path + "/" + name + "/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f :
        flag = False
        while True :
            line = f.readline().rstrip("\n")

            if not line : break
            if line[len(line)-1] == ',' : break
            if line[len(line)-1] == '-' : break
            if line[len(line)-1] == '.' : break

            dataF = line.split(",")
            # print(dataF)

            if len(dataF) < 4 : break
            # print(dataF[4])
            parsed = float(dataF[4])
            time = [[float(datum) for datum in dataF[0:3]]]

            # if len(parsed) != size:
            #     continue


            if not flag:
                data = np.array([parsed])
                timeStamp = np.array(time)
                flag = True
            else :
                data = np.append(data, [parsed], axis=0)
                timeStamp = np.append(timeStamp, time, axis=0)

        # print("Complete")
        if not flag :
            print("No Memory data")
            return
        if not os.path.exists("../" + name) :
            os.mkdir("../" + name)
        if not os.path.exists("../" + name + "/" + type) :
            os.mkdir("../" + name + "/" + type)
        sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat", {"timeStamp_" + type : timeStamp, type : data})

# phoneList = ["Iron2", "GalaxyS6", "GalaxyS7", "Vu2", "G5", "Nexus5X"]
#
# type = "Mem"
#
# for name in phoneList:
#     path = "D:/SmartCampusData" + "/" + name + "/CPSLogger/" + type
#     print(name)
#
#     fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#
#     for f in fileList:
#         dateFile = f[-14:-4]
#         # print(dateFile[5:7])
#         if int(dateFile[5:7]) < 5:
#             continue
#         print(dateFile)
#         extractAndSave(type, name, dateFile, 1)