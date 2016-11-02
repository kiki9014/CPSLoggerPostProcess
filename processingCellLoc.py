import numpy as np
import scipy.io as sio
import os.path

directoryPath = "D:/SmartCampusData"

def processingCell(dataF):
    if dataF[0] == "cellLoc":
        cellID = int(dataF[1])
        lac = int(dataF[2])
        psc = int(dataF[3])
        return [cellID, lac, psc]
    elif dataF[0] == "SignalStrength:" :
        return "null"
    else :
        return "null"


def extractAndSave (path, name, type, date):
    with open(path + "/" + name + "/CPSLogger/" + type + "/CPSLogger_" + type + "_" + date + ".txt", "r", encoding="utf8") as f :
        flag = False

        while True:
            line = f.readline().rstrip("\n")

            if not line: break
            if line[len(line) - 1] == ',': break
            if line[len(line) - 1] == '-': break
            if line[len(line) - 1] == '.': break

            dataF = line.split(",")

            # print(dataF)

            time = [float(timeChunk) for timeChunk in dataF[0:3]]

            content = dataF[3].split(" ")
            parsed = processingCell(content)

            if parsed == "null":
                continue

            dataFrag = time
            dataFrag.append(parsed[0])
            dataFrag.append(parsed[1])
            dataFrag.append(parsed[2])

            if not flag:
                data = np.array([dataFrag])
                flag = True
            else :
                data = np.append(data,[dataFrag], axis=0)

        if not os.path.exists("../" + name):
            os.mkdir("../" + name)
        if not os.path.exists("../" + name + "/" + type):
            os.mkdir("../" + name + "/" + type)
        if not flag:
            data = np.array([])
            flag = True
        if flag:
            sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat",
                        {type: data})

# type = "Signal"
#
# name = "Iron2"
#
# phoneList = ["Iron2", "GalaxyS6", "GalaxyS7", "Vu2", "G5", "Nexus5X"]
#
# for name in phoneList:
#     path = "D:/SmartCampusData" + "/" + name + "/CPSLogger/" + type
#     print(name)
#
#     fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
#
#     for f in fileList :
#         dateFile = f[-14:-4]
#         # print(dateFile[5:7])
#         if int(dateFile[5:7]) < 5 :
#             continue
#         print(dateFile)
#         extractAndSave(name, type, dateFile)