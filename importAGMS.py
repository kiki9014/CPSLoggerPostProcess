import numpy as np
import scipy.io as sio
import os.path

def dataArrange(line) :
    data = line.split(",")
    dataF = [float(datum) for datum in data]
    return dataF

## TODO : Implement This for simple code
#
# def line_gen(f):
#     while True:
#         line = f.readline()
#         if not line:
#             return
#         yield line
#
#
# with open as f:
#     x = line_gen(f)
#     y = map(dataArrange,x)
#     z = filter(lambda x: len(x) == 7)
#     .chop(100)
#
#     for chunk in x:
#         np.append(chunk)

def extractAndSave(path, type, name, date, size) :
    with open(path + name + "/CPSLogger" + "/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt", 'r') as f :
        index = 0

        buffer = []
        flag = False
        while True :
            line = f.readline()
            if not line : break
            if line[len(line)-1] == ',' : break
            if line[len(line)-1] == '-' : break
            if line[len(line)-1] == '.' : break

            parsed = dataArrange(line)
            if len(parsed) != size:
                continue

            buffer.append(parsed)

            if len(buffer) == 100000:
                if not flag:
                    data = np.array(buffer)
                    flag = True
                else :
                    data = np.append(data, buffer, axis=0)
                buffer = []
            index += 1
            if index%100000 == 0 :
                print(index)

        if not flag:
            data = np.array(buffer)
        else:
            data = np.append(data, buffer, axis=0)
        print("Complete")
        if not os.path.exists("../" + name) :
            os.mkdir("../" + name)
        if not os.path.exists("../" + name + "/" + type) :
            os.mkdir("../" + name + "/" + type)
        sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat", {type : data})

directoryPath = "D:/SmartCampusData/"
#
# date = "2016_05_18"
name = ["Iron2", "GalaxyS6", "GalaxyS7", "Vu2", "G5", "Nexus5X"]

for phone in name :
    path = directoryPath + phone + "/CPSLogger/Acc"

    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList :
        dateFile = f[-14:-4]
        extractAndSave("Acc",phone,dateFile,7)
        extractAndSave("Gyro",phone,dateFile,7)
        extractAndSave("Mag",phone,dateFile,7)
    # extractAndSave("Step",name,dateFile,5)

#
# with open(directoryPath+"/Acc/CPSLogger_Acc_2016_04_06.txt",'r') as f :
#     index = 0
#
#     buffer = []
#     flag = False
#     while True :
#         line = f.readline()
#         if not line : break
#
#         parsed = dataArrange(line)
#         if len(parsed) != 7:
#             continue
#
#         buffer.append(parsed)
#
#         if len(buffer) == 100000:
#             if not flag:
#                 data = np.array(buffer)
#                 flag = True
#             else :
#                 data = np.append(data, buffer, axis=0)
#             buffer = []
#         index += 1
#         if index%10000 == 0 :
#             print(index)
#
#     if not flag:
#         data = np.array(buffer)
#         flag = True
#     else:
#         data = np.append(data, buffer, axis=0)
#     buffer = []
#     print("Complete")
#     print(data[1][1])
#     sio.savemat("AccData.mat", {"Acc" : data})
# # print(data)