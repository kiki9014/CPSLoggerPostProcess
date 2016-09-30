import base64
import numpy as np
import scipy.io as sio
import os.path

directoryPath = "D:/SmartCampusData"

messengerList = ['com.kakao.talk','jp.naver.line.android','com.Slack','com.facebook.orca']
status = {'p' : 0, 'r' : 1}

# data structure
# time, type(0-SNS, 1-Noti, 2-Message), sender(-1 if type is noti), content, post/remove(0/1)

class UnexpectedError (Exception) :
    def __init__(self,value) :
        self.value = value

    def __str__(self):
        return repr(self.value)


def decodeWnull(text) :
    if text == "null" : return "null"
    else :
        # print(text)
        try :
            return base64.b64decode(text).decode("UTF-8")
        except (UnicodeDecodeError) :
            raise UnexpectedError("decode Failed")

def parsingContent(contentStr, time) :
    timeData = [float(timeChunk) for timeChunk in time]
    parsed = timeData
    # print(contentStr)
    if len(contentStr) == 1 : return "null"
    elif len(contentStr) == 3 : #SMS, MMS
        if (contentStr[0] != "SMS") & (contentStr[0] != "MMS") : return "error"
        sender = base64.b64decode(contentStr[1]).decode("UTF-8")
        contentLength = base64.b64decode(contentStr[2]).decode("UTF-8")
        if not contentLength.isnumeric() : contentLength = len(contentLength)
        parsed.append(2) # 2 means SMS and MMS
        parsed.append(int(sender))
        parsed.append(int(contentLength))
        parsed.append(0) # 0 means true(posted)
    elif len(contentStr) == 5 : #other notification
        try :
            content = [decodeWnull(contentChunk) for contentChunk in contentStr[:-2]]
        except UnexpectedError :
            return "error"
        if "error" in content :
            return "error"
        conLen = int(contentStr[-2])
        if content[0] in messengerList :
            parsed.append(0)
            parsed.append(int(content[2]))
        else :
            parsed.append(1)
            parsed.append(-1)
        if contentStr[-1] == "" :
            return "error"
        stat = status[contentStr[-1][0]]
        parsed.append(conLen)
        parsed.append(stat)
    else :
        return "error"
    return np.array([parsed])

def extractAndSave(date, name) :
    type = "Notification"
    with open(directoryPath+"/"+name+"/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt",'r') as f :

        flag = False

        while True :
            line = f.readline()

            if not line : break

            dataF = line.split(",")

            parsed = parsingContent(dataF[3:],dataF[:3])

            # print(parsed)

            if parsed == "null" : continue
            if parsed == "error" : break

            if not flag :
                data = np.array(parsed)
                flag = True
            else :
                data = np.append(data, parsed, axis=0)

        if not os.path.exists("../" + name):
            os.mkdir("../" + name)
        if not os.path.exists("../" + name + "/" + type):
            os.mkdir("../" + name + "/" + type)
        if flag :
            sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat", {type: data})


# date = "2016_05_18"
# name = ["Iron2", "GalaxyS4", "GalaxyS7", "Vu2"]
# name = "Iron2"

phoneList = ["Iron2", "GalaxyS4", "GalaxyS7", "Vu2", "G5", "Nexus5X"]

for name in phoneList :
    path = directoryPath + "/" + name + "/CPSLogger/Notification"
    fileList = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    for f in fileList :
        dateFile = f[-14:-4]
        # print(dateFile[5:7])
        if int(dateFile[5:7]) < 5 :
            continue
        print(dateFile)
        extractAndSave(dateFile, name)

# extractAndSave("2016_05_18", name)
# extractAndSave("2016_05_19", name)
# extractAndSave("2016_05_20", name)
# extractAndSave("2016_05_23", name)
# extractAndSave("2016_05_24", name)
# extractAndSave("2016_05_25", name)
# extractAndSave("2016_05_26", name)
# extractAndSave("2016_05_27", name)
# extractAndSave("2016_05_31", name)
# extractAndSave("2016_06_01", name)
# extractAndSave("2016_06_02", name)
# extractAndSave("2016_06_03", name)
# extractAndSave("2016_06_04", name)
# extractAndSave("2016_06_06", name)
# extractAndSave("2016_06_07", name)
# extractAndSave("2016_06_08", name)