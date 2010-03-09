from learning.correlation import pearson
from learning.fisher import fisher
from data.Loader import SortedMovieLoader
from data.Loader import SortedProbelessMovieLoader
from data.Loader import loadCorrelationLTM
from data.Serializer import *
from constants import *
import cProfile
from numpy import *
from time import *
from learning.overlap import overlap_count


def writePearsonMatrix():
    prefix = 'C:\\Netflix\kNN\\correlations\\rho_'
    oprefix = 'C:\\Netflix\kNN\\corrmatrix\\rho_'
    suffix = '.txt'
    
    startime = time()
    print "starting to process correlations at " + ctime(startime) 
     
    movies = range(1,mcount+1)
    for movieid in movies:
        corrfile = open(prefix+(str(movieid)).zfill(7)+suffix,'r')
        output = open(oprefix+(str(movieid)).zfill(7)+'.dat','w')
        
        rawlines = corrfile.readlines()
        rellines = rawlines[0:movieid-1] #relevant lines
        correlations = array([(double(x.strip())) for x in rellines])     
        correlations.dump(output)
        
        if movieid % 500 == 0:
            print ("%5.1f%%" % (100 * movieid/mcount)) + " of movies correlated..."
            print str((time()-startime)//60) + " minutes have passed"
        
        output.close()
        corrfile.close()

def cleanPearson(cdir):
    prefix = cdir+'\\rho_'
    suffix = '.txt'
    
    startime = time()
    print "starting to clean correlations at " + ctime(startime) 
    
    #this is kind of stupid since we're doing all the correlations twice, but I'm too tired to deal
    #with this right now...        
    movies = range(1,mcount+1)
    for movieid in movies:
        corrfilename = prefix+(str(movieid)).zfill(7)+suffix
        corrfile = open(corrfilename,'r')
        rawlines = corrfile.readlines()
        processed = [(x,'0\n')[x=='-1.#IND\n'] for x in rawlines]
        corrfile.close()
        corrfile = open(corrfilename,'w')
        corrfile.writelines(processed)
        
        if movieid % 500 == 0:
            print ("%5.1f%%" % (100 * movieid/mcount)) + " of movies correlated..."
            print str((time()-startime)//60) + " minutes have passed"

def writeProbePearson():  
    mindex = SortedProbelessMovieLoader()
    prefix = 'D:\\Netflix.Prize\\data\\probe.correlations\\rho_'
    suffix = '.txt'
    
    startime = time()
    print "starting to calculate correlations at " + ctime(startime) 
    
    #this is kind of stupid since we're doing all the correlations twice, but I'm too tired to deal
    #with this right now...        
    movies = range(1,mcount+1)
    for movieid in movies:
        corrfilename = prefix+(str(movieid)).zfill(7)+suffix
        corrfile = open(corrfilename,'w')
        cols = range(0,movieid)
        correlations = [str(pearson(mindex[movieid-1],mindex[x]))+"\n" for x in cols]
        corrfile.writelines(correlations)
        
        if movieid % 500 == 0:
            print ("%5.1f%%" % (100 * movieid/mcount)) + " of movies correlated..."
            print str((time()-startime)//60) + " minutes have passed"

def cached_Pearson(correlations,i,j):
    if i>j:
        return correlations[i][j]
    else:
        return correlations[j][i]

"""
    the number of customers who have seen both mi and mj
"""
def countOverlap(mi,mj):
    leni = len(mi)
    lenj = len(mj)

    n = 0
    i = 0
    j = 0

    while i<leni and j<lenj:
        Ci = mi[i]>>3
        Cj = mj[j]>>3
        if Ci == Cj:           
            i+=1
            j+=1
            n+=1
        elif Ci > Cj:
            j += 1
        else:
            i += 1 

    return n

def writeFisherZ():  
    mindex = SortedMovieLoader()
    correlations = loadCorrelationLTM(corrdir)
    prefix = 'C:\\Netflix\kNN\\fisherz\\z_'
    suffix = '.txt'
    
    startime = time()
    print "starting to calculate fisher z scores at " + ctime(startime) 

    movies = range(1,mcount+1)
    for movieid in movies:
        zfilename = prefix+(str(movieid)).zfill(7)+suffix
        zfile = open(zfilename,'w')
        cols = range(0,movieid)
        z_scores= [str(fisher(cached_Pearson(correlations,movieid-1,x),overlap_count(mindex[movieid-1],mindex[x])))+"\n" for x in cols]
        zfile.writelines(z_scores)
        
        if movieid % 500 == 0:
            print ("%5.1f%%" % (100 * movieid/mcount)) + " of movie correlations z-scored..."
            print str((time()-startime)//60) + " minutes have passed"        
            
def writeProbeFisherZ():  
    mindex = SortedProbelessMovieLoader()
    correlations = loadCorrelationLTM(probecorrdir)
    lprefix = 'D:\\Netflix.Prize\\data\\probe.fisherz.llimit\\z_'
    rprefix = 'D:\\Netflix.Prize\\data\\probe.fisherz.rlimit\\z_'
    suffix = '.txt'
    
    startime = time()
    print "starting to calculate fisher z scores at " + ctime(startime) 

    movies = range(1,mcount+1)
    for movieid in movies:
        lzfilename = lprefix+(str(movieid)).zfill(7)+suffix
        lzfile = open(lzfilename,'w')
        rzfilename = rprefix+(str(movieid)).zfill(7)+suffix
        rzfile = open(rzfilename,'w')        
        cols = range(0,movieid)
        z_scores= [fisher(cached_Pearson(correlations,movieid-1,x),overlap_count(mindex[movieid-1],mindex[x])) for x in cols]
        lz_scores = [str(x[0])+"\n" for x in z_scores]
        rz_scores = [str(x[1])+"\n" for x in z_scores]
        lzfile.writelines(lz_scores)
        rzfile.writelines(rz_scores)
        
        if movieid % 500 == 0:
            print ("%5.1f%%" % (100 * movieid/mcount)) + " of movie correlations z-scored..."
            print str((time()-startime)//60) + " minutes have passed"         
            
def cleanFisher(cdir):
    prefix = cdir+'\\z_'
    suffix = '.txt'
    
    startime = time()
    print "starting to clean correlations at " + ctime(startime) 
    
    #this is kind of stupid since we're doing all the correlations twice, but I'm too tired to deal
    #with this right now...        
    movies = range(1,mcount+1)
    for movieid in movies:
        corrfilename = prefix+(str(movieid)).zfill(7)+suffix
        corrfile = open(corrfilename,'r')
        rawlines = corrfile.readlines()
        processed = [(x,'0\n')[x=='-1.#IND\n'] for x in rawlines]
        corrfile.close()
        corrfile = open(corrfilename,'w')
        corrfile.writelines(processed)
        
        if movieid % 500 == 0:
            print ("%5.1f%%" % (100 * movieid/mcount)) + " of movies correlated..."
            print str((time()-startime)//60) + " minutes have passed"                     

writeProbeFisherZ()