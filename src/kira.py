from numpy import *
import learning.kNN
from data.Loader import *
from data.Serializer import *
from data.constants import *
import cProfile

def loadmain():
    qfile = open(qfilename,'r')
    qorder,qset = loadQualifyingSet(qfile)   
    lastsave = open(r'C:\Netflix\kNN\progress.txt','r')
    completed = lastsave.readlines()
    lastsave.close()
    lastdone = int((completed[len(completed)-1]).strip())
    sentinel = 0
    newqorder = empty(0,int)
    for x in qorder:
        if sentinel:
            newqorder = append(newqorder,x)
        if x == lastdone:
            sentinel = 1
    print lastdone
    print qorder[len(qorder)-1]
    print newqorder
    mindex,cindex = SortedTrainingLoader()
    predictions = open(r'C:\Netflix\kNN\predictions.txt','a')   
    progress = open(r'C:\Netflix\kNN\progress.txt','a')   
    learning.kNN.run(mindex,cindex,newqorder,qset,predictions,progress,15)

def main():
    qfile = open(qfilename,'r')
    qorder,qset = loadQualifyingSet(qfile)   
    mindex,cindex = SortedTrainingLoader() 
    correlations = loadFisherZLTM(fisherzdir)#loadCorrelationLTM(probecorrdir)
    predictions = open(r'C:\Netflix\kNN\predictions.txt','w')   
    progress = open(r'C:\Netflix\kNN\progress.txt','w')   
    learning.kNN.run(mindex,cindex,qorder,qset,predictions,progress,24,correlations)    

def probemain():
    qfile = open(probefilename,'r')
    qorder,qset = loadQualifyingSet(qfile)   
    #mindex,cindex = deserializeSortedProbeless()
    mindex,cindex = SortedProbelessTrainingLoader()
    correlations = loadFisherZLTM(probefisherzdir)
    predictions = open(r'D:\Netflix.Prize\predictions\kNN\predictions.txt','w')   
    progress = open(r'D:\Netflix.Prize\predictions\kNN\progress.txt','w')   
    learning.kNN.run(mindex,cindex,qorder,qset,predictions,progress,20,correlations)    
    
probemain()
#main()