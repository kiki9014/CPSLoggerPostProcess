import importEncodedData as iED
import os.path

name = "Iron2"

date = "2016_05_03"

def parseItem(entire) :
    first = entire.find(":")
    return entire[first+1:-1]

ts, data = iED.extract(name, "Clip", date, False, 5)

print(data)

print(parseItem(data[1]))