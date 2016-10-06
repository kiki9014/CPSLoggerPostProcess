import numpy as np
import scipy.io as sio
import os.path

directoryPath = "D:/SmartCampusData"

def extractAndSave (name, type, date):
    with open(directoryPath + "/" + name + "/CPSLogger/" + type + "/CPSLogger_" + type + "_" + date + ".txt", "r") as f :
        index = 0

        buffer = []

        flag = False

        while True :
            line = f.readline().rstrip("\n")

            if not line: break
            if line[len(line) - 1] == ',': break
            if line[len(line) - 1] == '-': break
            if line[len(line) - 1] == '.': break

            dataUid = line.split(",")

            if len(dataUid) < 5 : break
            # print(dataUid)

            time = [float(timeChunk) for timeChunk in dataUid[0:3]]

            if dataUid[-2] != "Uid" :
                continue

            lineTX = f.readline().rstrip("\n")
            if not lineTX : break
            if lineTX[-1] == ',' : break
            if lineTX[-1] == '-' : break
            lineRX = f.readline().rstrip("\n")
            if not lineRX : break
            if lineRX[-1] == ',' : break
            if lineRX[-1] == '-' : break

            dataTX = lineTX.split(",")
            if len(dataTX) < 5 : break
            dataRX = lineRX.split(",")
            if len(dataRX) < 5 : break

            uid = int(dataUid[-1])
            tx = int(dataTX[-1])
            rx = int(dataRX[-1])

            dataFrag = time

            dataFrag.append(uid)
            dataFrag.append(tx)
            dataFrag.append(rx)

            buffer.append(time)
            if len(buffer) == 100000:
                if not flag:
                    flag = True
                    data = np.array(buffer)
                else :
                    data = np.append(data, buffer, axis=0)
                buffer = []
            index += 1
            if index%10000 == 0 :
                print(index)

        if not os.path.exists("../" + name):
            os.mkdir("../" + name)
        if not os.path.exists("../" + name + "/" + type):
            os.mkdir("../" + name + "/" + type)
        if not flag:
            data = np.array(buffer)
            flag = True
        else:
            data = np.append(data, buffer, axis=0)
        if flag:
            sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat",
                        {type: data})

# name = "Iron2"

phoneList = ["Iron2", "GalaxyS6", "GalaxyS7", "Vu2", "G5", "Nexus5X"]

type = "Data"

for name in phoneList :
    path = "D:/SmartCampusData" + "/" + name + "/CPSLogger/" + type
    print(name)

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList :
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5 :
            continue
        print(dateFile)
        extractAndSave(name, type, dateFile)