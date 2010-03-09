from __future__ import division
import os
import cProfile
from data.Loader import ProbeLoader
from data.Loader import QualProbeLoader
from learning.kNN import *
from heapq import *
from learning.correlation import pearson
            
def main():
    k = 10
    mcount = 1
    
    cindex, mindex = ProbeLoader(r'E:\Netflix.Prize\data\conv.fullprobe.txt')
    qindex = QualProbeLoader(r'E:\Netflix.Prize\data\conv.fullprobe.txt')

    progressfile = open(r'E:\Netflix.Prize\movie.knn.probe.progress.txt','w')
    probepredictions = open(r'E:\Netflix.Prize\movie.probe.predictions.txt','w')   
    #progress = progressfile.readlines()
    
    start = 1
    """    if(len(progress)>0):
        ans = (raw_input("There is saved progress from a previous movie prediction run; continue from that point(y/n)? ")).strip()
        if(ans == 'y' or ans == 'Y'):
            start = int(progress[len(progress)-1])
            probepredictions = open(r'E:\Netflix.Prize\movie.probe.predictions.txt','a')
            progressfile = open(r'E:\Netflix.Prize\movie.knn.probe.progress.txt','a')
        else:
            probepredictions.close()
            progressfile.close()
            os.remove(r'E:\Netflix.Prize\movie.probe.predictions.txt')
            os.remove(r'E:\Netflix.Prize\movie.knn.probe.progress.txt')
            probepredictions = open(r'E:\Netflix.Prize\movie.probe.predictions.txt','w')            
            progressfile = open(r'E:\Netflix.Prize\movie.knn.probe.progress.txt','w')"""
        
            
    results = []
    
    predictions = {}
    
    print "starting the real work now..."
    
    for movieid in xrange(start,mcount+1):
        movie_predictions = []
        for customerid in qindex[movieid-1]:           
            # some funkiness where we filter out the current rating from the indexes to do loocv
            realmovie = mindex[movieid - 1]
            realcustomer = cindex[customerid]
            loocvmovie = filter(lambda x: x >> 3 != customerid,realmovie)
            loocvcustomer = filter(lambda x: x >> 3 != movieid,realcustomer)
            cindex[customerid] = loocvcustomer
            mindex[movieid-1] = loocvmovie
            #using heap here to keep neighbors in order of absolute value of correlation
            prating = kNNPrediction_Movie(pearson,movieid,loocvcustomer,mindex,customerid,k)       
            cindex[customerid] = realcustomer
            mindex[movieid-1] = realmovie
            movie_predictions.append(prating)
            
        if(len(movie_predictions)>0):    
            predictions[movieid] = movie_predictions
        if movieid % 300 == 0 or movieid == mcount:
            ids = (predictions.keys())
            ids.sort()
            for id in ids:
                probepredictions.write(str(id)+":\n")
                movie_predictions = [str(x)+"\n" for x in predictions[id]]
                probepredictions.writelines(movie_predictions)
            progressfile.write(str(ids[len(ids)-1])+"\n")
            progressfile.flush()
            predictions={}    
            print "Analyzed " + str(movieid) + " movies..."    
            

cProfile.run('main()')
#main()            