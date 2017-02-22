import numpy as np
import scipy.io as sio
import os.path
import sys

def dataArrange(line) :
    data = line.split(",")
    try :
        dataF = [float(datum) for datum in data]
    except ValueError :
        dataF = []
    return dataF

## Implement This for simple code => Try it if you have interest in simple code
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
    data = np.array([])
    try :
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
    except IOError as error:
        print("Error occurred when processing AGMS : {0}".format(error))
    except :
        print("Unexpected error occurred : " + sys.exc_info()[0])
    if not os.path.exists("../" + name) :
        os.mkdir("../" + name)
    if not os.path.exists("../" + name + "/" + type) :
        os.mkdir("../" + name + "/" + type)
    sio.savemat("../" + name + "/" + type + "/" + type + "_" + date + ".mat", {type : data})

directoryPath = "D:/SmartCampusData/"