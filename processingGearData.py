import numpy as np
import scipy.io as sio
import os.path
import sys

directoryPath = "D:/Data"

# Participant list
deviceIDList = ["P1", "P2", "P3", "P4", "P5"]

# As flag in gear data is started from 1, "None" is added
dataTypes = ["None", "gearAcc", "gearGyro", "gearMag", "gearUV", "gearLight", "gearPress", "gearHR", "gearBattery", "gearMemory"]
lenData = [0, 8, 8, 8, 6, 6, 6, 6, 6, 6]    # AGM data are three dimension vector

season4Date = "1_1"

def checkSeason(dateStr, seasonStr) :
    date = [int(dateChunk) for dateChunk in dateStr.split("_")]
    season = [int(seasonChunk) for seasonChunk in seasonStr.split("_")]

    if date[0] < season[0] :
        return False
    elif date[1] < season[1] :
        return False
    else :
        return True

def transGearToMat(path, name, date) :
    pathDir = path + "/" + date

    fileDir = [f for f in os.listdir(pathDir) if os.path.isfile(os.path.join(pathDir, f)) and f[0:9] == "HWsensing"]    # As HWsensing file and survey file are in same directory, extract list of HWSensing

    data = {}
    buffer = {}

    # Initialize data and buffer
    for type in dataTypes:
        data[type] = []
        buffer[type] = []

    flags = [False for type in dataTypes]

    try :
        for file in fileDir :   # As HWSensing file can be multiple files, for-loop is used
            with open(pathDir + "/" + file) as f:
                index = 0
                while True:
                    line = f.readline().rstrip('\n') # If problem is occurred, remove ".rstrip('\n')"

                    if not line : break
                    if line[len(line)-1] == "-" : break
                    if line[len(line)-1] == ',' : break
                    if line[len(line)-1] == '.' : break

                    dataF = line.split(",")

                    if len(dataF) < 5 : break

                    if len(dataF) < lenData[int(dataF[4])] : break

                    # Change dimension of time vector from 4 to 3
                    time = [float(timeChunk) for timeChunk in dataF[0:4]]
                    time[2] = time[2] + time[3]/1000
                    del time[3]

                    # Get data flag from read line
                    dataTypeNum = int(dataF[4])
                    # Change string data to array of float
                    dataFragments = [float(dataFrag) for dataFrag in dataF[5:]]
                    # Merge time and data
                    time.extend(dataFragments)

                    dataChunk = time
                    # Get type of data
                    dataType = dataTypes[dataTypeNum]
                    # Buffer is needed to boost processing speed
                    buffer[dataType].append(dataChunk)

                    flag = flags[dataTypeNum]
                    # Save buffer to matrix
                    if len(buffer[dataType]) == 100000 :
                        # print(dataType)
                        if not flag :
                            data[dataType] = np.array(buffer[dataType])
                            flags[dataTypeNum] = True
                        else :
                            data[dataType] = np.append(data[dataType], buffer[dataType], axis=0)
                        buffer[dataType] = []

                    index += 1
                    if index%100000 == 0:
                        print(index)
    except IOError as error :
        print("Error occurred when processing Gear data : {0}".format(error))
    except :
        print("Unexpected error occurred : " + sys.exc_info()[0])
    # Set empty space to empty data
    for dataType in dataTypes :
        if not flags[dataTypes.index(dataType)]:
            data[dataType] = np.array(buffer[dataType])
        else:
            data[dataType] = np.append(data[dataType], buffer[dataType], axis=0)

    del data["None"]

    if not os.path.exists("../" + name):
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + date) :
        os.mkdir("../" + name + "/" + date)
    sio.savemat("../" + name + "/" + date + "/" + "gearSensing_" + date + ".mat", data)

for deviceID in deviceIDList :
    path = directoryPath + "/" + deviceID + "/Gear"
    print(deviceID)
    dirList = [d for d in os.listdir(path) if not os.path.isfile(os.path.join(path, d))]
    for dir in dirList :
        date = dir
        if checkSeason(date, season4Date) == False :
            continue
        print(date)
        transGearToMat(path, deviceID, date)
