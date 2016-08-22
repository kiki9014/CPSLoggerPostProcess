import base64
import numpy as np
import scipy.io as sio

directoryPath = "D:/CPSLogger"

def extractAndSave(date, name) :
    type = "Notification"
    with open(directoryPath+"/" + type + "/" + "CPSLogger_" + type + "_" + name + ".txt",'r') as f :
        while True :
            line = f.readline()

            if not line : break

            dataF = line.split(",")

            print(dataF)

date = "2016_05_18"
name = "Iron2"

extractAndSave(date, name)