from numpy import *
from data.constants import *
from data.Loader import *
from learning.correlation import pearson

def test1():   
    mindex = SortedMovieLoader() 
    correlations = loadCorrelationLTM()
    
    print correlations[200].dtype.name
    
    if correlations[500][1] - pearson(mindex[500],mindex[1]) > 0.00001:
        print 'test 1 FAILED ' + str((correlations[500][1],pearson(mindex[500],mindex[1])))
    else:
        print 'test 1 passed ' + str((correlations[500][1],pearson(mindex[500],mindex[1])))
    if correlations[499][498] - pearson(mindex[498],mindex[499]) > 0.00001:
        print 'test 1 FAILED ' + str((correlations[499][498],pearson(mindex[499],mindex[498])))
    else:
        print 'test 1 passed ' + str((correlations[499][498],pearson(mindex[499],mindex[498])))
    if correlations[15000][10] - pearson(mindex[15000],mindex[10]) > 0.00001:
        print 'test 1 FAILED ' + str((correlations[15000][10],pearson(mindex[15000],mindex[10])))
    else:
        print 'test 1 passed ' + str((correlations[15000][10],pearson(mindex[15000],mindex[10])))
    if correlations[2][1] - pearson(mindex[1],mindex[2]) > 0.00001:
        print 'test 1 FAILED ' + str((correlations[2][1],pearson(mindex[1],mindex[2])))
    else:
        print 'test 1 passed ' + str((correlations[2][1],pearson(mindex[1],mindex[2])))