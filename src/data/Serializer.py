from data.Loader import *
from data.constants import *
import cPickle

def serializeSortedProbeless():
    mindex, cindex = SortedProbelessTrainingLoader()
    
    startime = time()
    
    print "starting to serialize training set at " + ctime(startime)          

    filename = mnoprobe_dir_pkl + 'mindex.dat'
    moviefile = open(filename,'w')
    
    cfilename = cnoprobe_dir_pkl + 'cindex.dat'
    custfile = open(cfilename,'w')    
    
    cPickle.dump(mindex,moviefile)

    print "Done serializing movie set at " + str((time()-startime)//60)    
    
    cPickle.dump(cindex,custfile)
    
    print "Done serializing customer set at " + str((time()-startime)//60)

def serializeSortedTrainingSet():
    mindex, cindex = SortedTrainingLoader()
    
    startime = time()
    
    print "starting to serialize training set at " + ctime(startime)          

    filename = msorted_dir_pkl + 'mindex.dat'
    moviefile = open(filename,'w')
    
    cfilename = csorted_dir_pkl + 'cindex.dat'
    custfile = open(cfilename,'w')    
    
    cPickle.dump(mindex,moviefile)

    print "Done serializing movie set at " + str((time()-startime)//60)    
    
    cPickle.dump(cindex,custfile)
    
    print "Done serializing customer set at " + str((time()-startime)//60) 

def deserializeSortedMovies():
    startime = time()    
    
    filename = msorted_dir_pkl + 'mindex.dat'
    moviefile = open(filename,'r')
    
    print "starting to deserialize movie set at " + ctime(startime)
    mindex = cPickle.load(moviefile)
    print "Done deserializing movie set at " + str((time()-startime)//60)
    
    return mindex

def deserializeSortedProbeless():
    startime = time()    
    
    filename = mnoprobe_dir_pkl + 'mindex.dat'
    moviefile = open(filename,'r')
    
    cfilename = cnoprobe_dir_pkl + 'cindex.dat'
    custfile = open(cfilename,'r')
    
    print "starting to deserialize movie set at " + ctime(startime)
    mindex = cPickle.load(moviefile)
    print "Done deserializing movie set at " + str((time()-startime)//60)
    print "starting to deserialize customer set at " + str((time()-startime)//60)
    cindex = cPickle.load(custfile)    
    print "Done deserializing customer set at " + str((time()-startime)//60)
    
    return (mindex,cindex)

def deserializeSortedTrainingSet():
    startime = time()    
    
    filename = msorted_dir_pkl + 'mindex.dat'
    moviefile = open(filename,'r')
    
    cfilename = csorted_dir_pkl + 'cindex.dat'
    custfile = open(cfilename,'r')
    
    print "starting to deserialize movie set at " + ctime(startime)
    mindex = cPickle.load(moviefile)
    print "Done deserializing movie set at " + str((time()-startime)//60)
    print "starting to deserialize customer set at " + str((time()-startime)//60)
    cindex = cPickle.load(custfile)    
    print "Done deserializing customer set at " + str((time()-startime)//60)
    
    return (mindex,cindex)

def deserializeFisherZ(dir):
    startime = time()    
    
    filename = dir + 'fisherz.dat'
    file = open(filename,'r')
    
    print "starting to deserialize fisherz data at " + ctime(startime)
    fisherz = cPickle.load(file)
    print "Done deserializing movie set at " + str((time()-startime)//60)

    return fisherz

def serializeFisherZ(sdir,ddir):
    fisherz = loadFisherZLTM(sdir)
    
    startime = time()    
    
    filename = ddir + 'fisherz.dat'
    file = open(filename,'w')
    
    print "starting to serialize fisherz correlations at " + ctime(startime)
    cPickle.dump(fisherz,file)
    print "Done serializing fisherz correlations at " + str((time()-startime)//60)

#serializeSortedTrainingSet()
#serializeSortedProbeless()
#serializeFisherZ(probefisherzdir,probefisherzpkl)