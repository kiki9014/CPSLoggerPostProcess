import numpy as np
import scipy.io as sio
import os.path

defaultDir = "D:/ActionLocationDataset/"

def croppingGearFile(name, date) :
    with open(defaultDir + name + "/Gear" + date) :
        print(name)