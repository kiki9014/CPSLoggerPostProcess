import numpy as np
import scipy.io as sio
import os.path
import operator
from sklearn import svm
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt

directoryPath = "C:/Users/Hyunjun/Documents/MATLAB/Gear"

value = ["Moodscope", "Boreapp", "MONARCA", "Jigsaw"]

def num2feature(number) :
    binNum = "{0:04b}".format(number)

    numArr = [int(binary) for binary in binNum]

    # print(numArr[3])

    code =  str(numArr[0]) + "  " + str(numArr[1]) + "  " + str(numArr[2]) + "  " + str(numArr[3])

    featureList = [value[i] for i in range(4) if numArr[i] == 1]
    return featureList, code

def oneStepSVMByFeat(number, type, date) :
    featureList, code = num2feature(number)

    print("SVM with " + str(featureList))

    mat = sio.loadmat(directoryPath+"/" + date + "/"+ type +"/truncfeature_" + code + "_" + type + ".mat")

    trainData = mat['trainData']
    testData = mat['testData']

    trainFeat = trainData[:,1:]
    testFeat = testData[:,1:]
    trainLab = trainData[:,0]
    testLab = testData[:,0]

    clf = svm.SVC(probability=True)
    clf.fit(trainFeat, trainLab)

    cSpace = np.logspace(-20,20,num=80,base=2.0)
    gSpace = np.logspace(-20,20,num=80,base=2.0)

    paramGrid = dict(gamma = gSpace,C = cSpace)
    cv = StratifiedShuffleSplit(trainLab,test_size=0.2, random_state=42)
    grid = GridSearchCV(svm.SVC(), param_grid= paramGrid, cv=cv)
    grid.fit(trainFeat, trainLab)

    print("Best param : %s with score %0.2f" % (grid.best_params_,grid.best_score_))

    bestClf = grid.best_estimator_

    predictLab = bestClf.predict(testFeat)

    cm = confusion_matrix(testLab, predictLab)

    print(cm)

    cmNorm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    print(cmNorm)

    accuracy = accuracy_score(testLab, predictLab)

    print("Accuracy : " + str(accuracy))

    prec = precision_score(testLab, predictLab)

    print("Precision : " + str(prec))

    reca = recall_score(testLab,predictLab)

    print("Recall :" + str(reca))

    decisionFunc = bestClf.decision_function(testFeat)

    precision, recall, _ = precision_recall_curve(testLab, decisionFunc)

    # plt.clf()

    return [accuracy, cm, cmNorm, prec, reca, decisionFunc, precision, recall]

binNum = "{0:04b}".format(4)
test = (binNum)
print((binNum))

accA = []
accH = []

# awakeness = oneStepSVMByFeat(2, 'awakeness')

# print("In awakeness, max accuracy is from %s features with %0.2f score" % (num2feature(1)[0], 0.321))

date = "2016_10_20"

for i in range(1,16) :
    awakeness = oneStepSVMByFeat(i, "awakeness", date)
    accA.append(awakeness[0])
    happiness = oneStepSVMByFeat(i, "happiness", date)
    accH.append(happiness[0])

    frag = [awakeness[0], happiness[0]]

    cm = [awakeness[1], happiness[1]]

    prec = [awakeness[3], happiness[3]]

    rec = [awakeness[4], happiness[4]]

    dec = [awakeness[5], happiness[5]]

    plt.figure(2*i-1);
    plt.plot(awakeness[7], awakeness[6], label='Precision-Recall curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.xlim([0.0, 1.1])
    plt.ylim([0.0, 1.1])
    plt.title("Precision-Recall curve for " + "activeness" + " with " + str(i))
    plt.show(block=False)

    plt.figure(2*i);
    plt.plot(happiness[7], happiness[6], label='Precision-Recall curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.xlim([0.0, 1.1])
    plt.ylim([0.0, 1.1])
    plt.title("Precision-Recall curve for " + "happiness" + " with " + str(i))
    plt.show(block=False)

    if i == 1 :
        result = np.array([frag])
        confM = np.array([cm])
        precision = np.array([prec])
        recall = np.array([rec])
        decision = np.array([dec])
    else :
        result = np.append(result, [frag], axis=0)
        confM = np.append(confM, [cm], axis=0)
        precision = np.append(precision, [prec], axis=0)
        recall = np.append(recall, [rec], axis=0)
        decision = np.append(decision, [dec], axis=0)

idxA, maxAccA = max(enumerate(accA), key=operator.itemgetter(1))
idxH, maxAccH = max(enumerate(accH), key=operator.itemgetter(1))

print("In awakeness, max accuracy is from %s features with %0.2f score" % (num2feature(idxA+1)[0], maxAccA))
print("In happiness, max accuracy is from %s features with %0.2f score" % (num2feature(idxH+1)[0], maxAccH))

sio.savemat(directoryPath + "/" + date + "_Truncresult.mat", {"accTable" : result, "confusionMatrix" : confM, "precision" : precision, "recall" : recall, "decisionFunc" : decision})