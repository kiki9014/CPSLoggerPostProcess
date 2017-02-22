import base64
import numpy as np
import scipy.io as sio
import os.path
import sys

# Classify notifications
messengerList = ['com.kakao.talk','jp.naver.line.android','com.Slack','com.facebook.orca']
status = {'p' : 0, 'r' : 1}     # 'p' : posted, 'r' : read

notiType = ['Messenger', 'Notification', 'SMS'] # 'Messenger' : SNS, 'Notification' : neither SNS or SMS

# Initialize count of sender
cntSender = {}
cntSender["Messenger"] = {}
cntSender["SMS"] = {}

# Count function
def countSender (name, type, sender) :
    if sender in cntSender[type][name] :
        cntSender[type][name][sender] += 1
    else :
        cntSender[type][name][sender] = 1

# For convenience (not used)
class UnexpectedError (Exception) :
    def __init__(self,value) :
        self.value = value

    def __str__(self):
        return repr(self.value)

# If array has null and encoded string both, decode separately
def decodeWnull(text) :
    if text == "null" : return "null"
    else :
        try :
            return base64.b64decode(text).decode("UTF-8")
        except (UnicodeDecodeError) :
            raise UnexpectedError("decode Failed")

# Parsing function
def parsingContent(contentStr, time) :
    timeData = [float(timeChunk) for timeChunk in time]
    parsed = timeData
    if len(contentStr) == 1 : return "null"
    elif len(contentStr) == 3 : # SMS, MMS
        if (contentStr[0] != "SMS") & (contentStr[0] != "MMS") : return "error"
        sender = base64.b64decode(contentStr[1]).decode("UTF-8")
        contentLength = base64.b64decode(contentStr[2]).decode("UTF-8")
        if not contentLength.isnumeric() : contentLength = len(contentLength) # In old version, contentLength is content instead of length
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
    return np.array(parsed)

def extractAndSave(path, date, name) :
    type = "Notification"
    flag = False

    try :
        with open(path+"/"+name+"/CPSLogger/" + type + "/" + "CPSLogger_" + type + "_" + date + ".txt",'r') as f :

            while True :
                line = f.readline().rstrip('\n') # If error occurred, erase ".rstrip('\n')"

                if not line : break

                dataF = line.split(",")

                parsed = parsingContent(dataF[3:],dataF[:3])

                if parsed == "null" : continue
                if parsed == "error" : break

                if parsed  != "null" :
                    sender = parsed[4]
                    if parsed[3] != 1 :
                        countSender(name, notiType[int(parsed[3])],sender)

                if not flag :
                    data = np.array([parsed])
                    flag = True
                else :
                    data = np.append(data, [parsed], axis=0)

    except IOError as error :
        print("Error occurred when processing notification : {0}".format(error))
    except :
        print("Unexpected error occurred : " + sys.exc_info()[0])
    if not flag :
        data = np.array([])
    if not os.path.exists("../" + name):
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + type) :
        os.mkdir("../" + name + "/" + type)
    if flag :
        sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat", {type: data})

def initCount(name) :
    cntSender["Messenger"][name] = {}
    cntSender["SMS"][name] = {}

def saveCount(nameList) :
    if not os.path.exists("../common") :
        os.mkdir("../common")
    MessengerList = {}
    SMSList = {}

    for name in nameList :
        MessengerList[name + "_MessengerList"] = list(cntSender["Messenger"][name].items())
        SMSList[name+ "_SMSList"] = list(cntSender["SMS"][name].items())

    sio.savemat("../common/SNS.mat", MessengerList)
    sio.savemat("../common/SMS.mat", SMSList)
