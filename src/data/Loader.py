from __future__ import division
from datetime import date
from time import *
from numpy import *
from data.constants import *

"""
    Return a tuple consisting of training data indexed by movie and customer
    Indices are lists of NumPy arrays
"""
def initIndices(mcount, ccount):
    movieindex = []
    customerindex = []
    
    for i in range(0,mcount):
        movieindex.append(empty(0,int))
    for i in range(0,ccount):
        customerindex.append(empty(0,int))
        
    return (movieindex,customerindex)

"""
    processes linedata, returns a tuple of the rating packed first with movie id, then with
    customer id, then customer id
"""
def lineProcesser(line,movie):
    linedata = line.split(",")
    cid = int(linedata[0]) << 3
    rating = int(linedata[1])
    mpackage = cid | rating
    mid = movie << 3
    cpackage = mid | rating
    return (mpackage,cpackage,int(linedata[0]))
    
def sortIndices(movieindex,customerindex):
    for i in range(0,len(movieindex)):
        tmplist = movieindex[i].tolist()
        tmplist.sort(PackedRatingCompare)
        movieindex[i] = array(tmplist)
    for i in range(0,len(customerindex)):
        tmplist = customerindex[i].tolist()
        tmplist.sort(PackedRatingCompare)
        customerindex[i] = array(tmplist)    

"""
    Return two nested structures, one keyed by customer id, one keyed by movie id,
    for training
"""
def ProbeLoader(filename):
    movieindex, customerindex = initIndices(mcount,ccount)
            
    probefile = open(filename, 'r')
    for line in probefile:       
        probeline = line.strip()
        if probeline.endswith(':'): #begin movie data
            movie = int(line.replace(":",""))
            if movie>mcount:
                break
        else: #this is a customer rating
            mpackage,cpackage,custid = lineProcesser(line,movie)            
            movieindex[movie-1] = append(movieindex[movie-1],mpackage)
            customerindex[custid] = append(customerindex[custid],cpackage)                                    

    print "Probe set fully loaded into memory.  Now beginning the sort..."
    sortIndices(movieindex,customerindex)
    
    print "Finished sorting, returning now."        
    return (customerindex, movieindex)                                

"""
    Same as above, but meant to load the probe data as a qualifying set
"""
def QualProbeLoader(filename):    
    movieindex = []
    for i in range(0,mcount):
        movieindex.append(array('L'))
    probefile = open(filename, 'r')
    for line in probefile:
        probeline = line.strip()
        if probeline.endswith(':'): #begin movie data
            movie = int(line.replace(":",""))
            if movie>mcount:
                break
        else: #this is a customer rating
            linedata = line.split(",")
            cid = int(linedata[0])
            movieindex[movie-1].append(cid)
    print "done loading customer/movie qualifying data into memory"
    return movieindex

"""
    load the sorted training set
"""
def SortedProbelessMovieLoader(): 
    startime = time()
    print "starting to load training set at " + ctime(startime) 
    movieindex,customerindex = initIndices(mcount,ccount)           
    
    for movie in range(1,mcount+1):
        filename = mnoprobe_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')  
        
        rawdata = moviefile.readlines()
        del rawdata[0]
        moviedata = [int(x.strip()) for x in rawdata]          
        movieindex[movie-1] = array(moviedata)              
               
        if movie % 500 == 0:
            print "Training set movies" + ("%5.1f%%" % (100 * movie/mcount)) + " loaded..."
            print str((time()-startime)//60) + " minutes have passed"

        moviefile.close()    

    return movieindex

"""
    load the sorted training set
"""
def SortedMovieLoader(): 
    startime = time()
    print "starting to load training set at " + ctime(startime) 
    movieindex,customerindex = initIndices(mcount,ccount)           
    
    for movie in range(1,mcount+1):
        filename = msorted_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')  
        
        rawdata = moviefile.readlines()
        del rawdata[0]
        moviedata = [int(x.strip()) for x in rawdata]          
        movieindex[movie-1] = array(moviedata)              
               
        if movie % 500 == 0:
            print "Training set movies" + ("%5.1f%%" % (100 * movie/mcount)) + " loaded..."
            print str((time()-startime)//60) + " minutes have passed"

        moviefile.close()    

    return movieindex

"""
    load the sorted training set
"""
def SortedTrainingLoader(): 
    startime = time()
    print "starting to load training set at " + ctime(startime) 
    movieindex,customerindex = initIndices(mcount,ccount)           
    
    for movie in range(1,mcount+1):
        filename = msorted_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')  
        
        rawdata = moviefile.readlines()
        del rawdata[0]
        moviedata = [int(x.strip()) for x in rawdata]          
        movieindex[movie-1] = array(moviedata)              
               
        if movie % 500 == 0:
            print "Training set movies" + ("%5.1f%%" % (100 * movie/mcount)) + " loaded..."
            print str((time()-startime)//60) + " minutes have passed"

        moviefile.close()    

    customer = -1
    clist = []
    for group in range(0,490000,10000):
        filename = csorted_dir + 'c_'+(str(group))+'.txt'
        file = open(filename,'r')
        rawdata = file.readlines()
        for rawline in rawdata:
            line = rawline.strip()            
            if line.endswith(':'): #begin movie data
                if customer != -1:
                    customerindex[customer] = array(clist)
                    clist = []
                customer = int(line.replace(":",""))
                if customer % 10000 == 0:
                    print "Training set customers" + ("%5.1f%%" % (100 * customer/ccount)) + " loaded..."
                    print str((time()-startime)//60) + " minutes have passed"
                    
            else:
                clist.append(int(line))
        customerindex[customer] = array(clist)
        file.close()

    return (movieindex,customerindex)

"""
    load the sorted training set--probeless
"""
def SortedProbelessUserLoader(): 
    startime = time()
    print "starting to load training set at " + ctime(startime) 
    movieindex,customerindex = initIndices(mcount,ccount)           
    
    customer = -1
    clist = []
    for group in range(0,490000,10000):
        filename = cnoprobe_dir + 'c_'+(str(group))+'.txt'
        file = open(filename,'r')
        rawdata = file.readlines()
        for rawline in rawdata:
            line = rawline.strip()            
            if line.endswith(':'): #begin movie data
                if customer != -1:
                    customerindex[customer] = array(clist)
                    clist = []
                customer = int(line.replace(":",""))
                if customer % 10000 == 0:
                    print "Training set customers" + ("%5.1f%%" % (100 * customer/ccount)) + " loaded..."
                    print str((time()-startime)//60) + " minutes have passed"
                    
            else:
                clist.append(int(line))
        customerindex[customer] = array(clist)
        file.close()

    return customerindex

"""
    load the sorted training set--probeless
"""
def SortedProbelessTrainingLoader(): 
    startime = time()
    print "starting to load training set at " + ctime(startime) 
    movieindex,customerindex = initIndices(mcount,ccount)           
    
    for movie in range(1,mcount+1):
        filename = mnoprobe_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')  
        
        rawdata = moviefile.readlines()
        del rawdata[0]
        moviedata = [int(x.strip()) for x in rawdata]          
        movieindex[movie-1] = array(moviedata)              
               
        if movie % 500 == 0:
            print "Training set movies" + ("%5.1f%%" % (100 * movie/mcount)) + " loaded..."
            print str((time()-startime)//60) + " minutes have passed"

        moviefile.close()    

    customer = -1
    clist = []
    for group in range(0,490000,10000):
        filename = cnoprobe_dir + 'c_'+(str(group))+'.txt'
        file = open(filename,'r')
        rawdata = file.readlines()
        for rawline in rawdata:
            line = rawline.strip()            
            if line.endswith(':'): #begin movie data
                if customer != -1:
                    customerindex[customer] = array(clist)
                    clist = []
                customer = int(line.replace(":",""))
                if customer % 10000 == 0:
                    print "Training set customers" + ("%5.1f%%" % (100 * customer/ccount)) + " loaded..."
                    print str((time()-startime)//60) + " minutes have passed"
                    
            else:
                clist.append(int(line))
        customerindex[customer] = array(clist)
        file.close()

    return (movieindex,customerindex)

def loadQualifyingSet(qfile):
    qdata = []
    qorder = empty(0,int)
    qraw = qfile.readlines()
    counter = 0
    
    for i in range(0,mcount):
        qdata.append(empty(0,int))

    movie = 1    
    
    for line in qraw:
        qline = line.strip()
        if qline.endswith(':'): #begin movie data
            movie = int(line.replace(":",""))
            qorder = append(qorder,movie) #should i store movie or movie-1?  remember that this is real movie id!
        else: #this is a customer rating
            counter += 1
            linedata = line.split(",")
            cid = int(linedata[0])
            qdata[movie-1] = append(qdata[movie-1],cid)

    print "Read in " + str(counter) + " ratings to be predicted."
    return (qorder,qdata)

"""
    DEPRECATED
"""
def TrainingLoader(): 
    startime = time()
    print "starting to load training set at " + ctime(startime) 
    movieindex = []
    customerindex = []    
    for i in range(0,mcount):
        movieindex.append(array('L'))
    for i in range(0,ccount):
        customerindex.append(array('L'))            
    
    for movie in range(1,mcount+1):
        filename = converted_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')  
        
        rawdata = moviefile.readlines()
        del rawdata[0]    
        
        for rawline in rawdata:
            linedata = (rawline.strip()).split(',')
            cid = int(linedata[0]) << 3
            rating = int(linedata[1])
            mpackage = cid | rating
            movieindex[movie-1].append(mpackage)
            mid = movie << 3
            cpackage = mid | rating
            customerindex[int(linedata[0])].append(cpackage)                        
               
        if movie % 500 == 0:
            print "Training set " + ("%5.1f%%" % (100 * movie/mcount)) + " loaded..."
            print str((time()-startime)//60) + " minutes have passed"

        moviefile.close()    
            
    print "Training set fully loaded into memory.  Now beginning the sort..."
    
    for i in range(0,mcount):
        tmplist = movieindex[i].tolist()
        tmplist.sort(PackedRatingCompare)
        movieindex[i] = array('L')
        movieindex[i].fromlist(tmplist)
        if i % 500 == 0:
            print "Movie index " + ("%5.1f%%" % (100 * i/mcount)) + " sorted..."
            print str((time()-startime)//60) + " minutes have passed"
    for i in range(0,ccount):
        tmplist = customerindex[i].tolist()
        tmplist.sort(PackedRatingCompare)
        customerindex[i] = array('L')
        customerindex[i].fromlist(tmplist)
        if i % 500 == 0:
            print "Customer index " + ("%5.1f%%" % (100 * i/ccount)) + " sorted..."
            print str((time()-startime)//60) + " minutes have passed"                  
        
    print "Finished sorting, returning now."
        
    return (customerindex,movieindex)

"""
    compares the id portions of r1 and r2 and sorts accordingly
"""
def PackedRatingCompare(r1,r2):
    rv = (r1 >> 3) - (r2 >> 3)
    return int(rv)

"""
    binary searches an array of id/rating pairs, returns the index if found, -1 if does not exist in array
"""
def customerArrayBinarySearch(a,target,lbound,ubound):
    length = ubound-lbound
    midpoint = length//2 + lbound
    if a[midpoint] == target:
        return midpoint
    elif ubound <= lbound:
        return -1
    elif a[midpoint] > target:
        return customerArrayBinarySearch(a,target,lbound,midpoint-1)
    else:
        return customerArrayBinarySearch(a,target,midpoint+1,ubound)        

"""
    DEPRECATED
"""
def QualTrainLoader(): 
    startime = time()
    print "starting to load training set at " + ctime(startime) 
    
    for movie in range(1,mcount+1):
        filename = converted_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')  
        
        rawdata = moviefile.readlines()
        del rawdata[0]    
        processed = array('L')
        
        for rawline in rawdata:
            linedata = (rawline.strip()).split(',')
            cid = int(linedata[0]) << 3
            rating = int(linedata[1])
            mpackage = cid | rating
            processed.append(mpackage)
            
        moviefile.close()
        
        yield processed               
            
"""
    only need this once; make the set of customer id's continuous for the sake of my sanity
"""
def customerRegistry():
    startime = time()
    print "starting to convert customer id's " + ctime(startime) 
    cindex = {}       
    
    for movie in range(1,mcount+1):
        filename = train_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')  
        
        rawdata = moviefile.readlines()
        del rawdata[0]    
        
        for rawline in rawdata:
            linedata = (rawline.strip()).split(',')
            cid = int(linedata[0])
            if not cindex.has_key(cid):
                cindex[cid] = len(cindex.keys())
               
        if movie % 500 == 0:
            print "Data set " + ("%5.1f%%" % (100 * movie/mcount)) + " scanned..."
            print str((time()-startime)//60) + " minutes have passed"
        
        moviefile.close()    
            
    print "Data scan complete.\nThere are " + str(len(cindex.keys())) + " customers in the data set."
    
    keyfile = open(r'E:\Netflix.Prize\keylist.txt','w')
    for cid in cindex.keys():
        keyfile.write(str((cid,cindex[cid]))+'\n')
        
"""
    companion to the above function, loads the structure represented by the flat file into memory
"""
def loadCustomerRegistry():
    startime = time()
    print "starting to load customer id's " + ctime(startime) 
    cindex = {}       
    
    keyfile = open(r'D:\Netflix.Prize\keylist.txt','r')
    keylines = keyfile.readlines()
    for keyline in keylines:
        keyline = keyline.strip(' ()\n')
        keypair = keyline.split(',')
        cindex[int(keypair[0])]=int(keypair[1])

    print "Customer id's have been loaded."
    print cindex[1808649]
    print cindex[1488844]
    return cindex

"""
    hopefully only need this once...
"""
def outputSortedTrainingSet():
    startime = time()    
    cindex, mindex = TrainingLoader()
    print "starting to write sorted movie index..." + ctime(startime)       
    
    for movie in range(1,mcount+1):
        filename = msorted_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        file = open(filename,'w')
        file.write(str(movie)+":\n")
        
        for rpair in mindex[movie-1]:
            file.write(str(rpair)+"\n")
               
        if movie % 500 == 0:
            print "Sorted movie index " + ("%5.1f%%" % (100 * movie/mcount)) + " converted..."
            print str((time()-startime)//60) + " minutes have passed"

        file.close()

    group = 0

    filename = csorted_dir + 'c_'+(str(group))+'.txt'
    file = open(filename,'w')

    for customer in range(0,ccount):
        if customer>(group+10000):
            file.close()
            group += 10000
            print "Sorted customer index " + ("%5.1f%%" % (100 * customer/ccount)) + " converted..."
            print str((time()-startime)//60) + " minutes have passed"            
            filename = csorted_dir + 'c_'+(str(group))+'.txt'
            file = open(filename,'w')

        file.write(str(customer)+":\n")
        
        for rpair in cindex[customer]:
            file.write(str(rpair)+"\n")                        
            
    print "Sorted training set written."

"""
    hopefully only need this once; replace the original customer id's in the training set with
    the continuous set I generated
"""
def convertCustomerRegistry():
    startime = time()
    print "starting to convert customer id's in the training set " + ctime(startime) 
    cindex = loadCustomerRegistry()       
    
    for movie in range(1,mcount+1):
        filename = train_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        cfilename = converted_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')
        cfile = open(cfilename,'w')  
        
        rawdata = moviefile.readlines()
        cfile.write(rawdata[0])
        del rawdata[0]    
        
        for rawline in rawdata:
            linedata = (rawline.strip()).split(',')
            cfile.write(str(cindex[int(linedata[0])])+","+linedata[1]+","+linedata[2]+"\n")
               
        if movie % 500 == 0:
            print "Training set " + ("%5.1f%%" % (100 * movie/mcount)) + " converted..."
            print str((time()-startime)//60) + " minutes have passed"
        
        moviefile.close()
        cfile.close()    
            
    print "Training set customer id's fully converted."
    
"""
    hopefully only need this once; replace the original customer id's in the qualifying set with
    the continuous set I generated
"""
def convertQualifyingSet():
    startime = time()
    print "starting to convert customer id's in the qualifying set " + ctime(startime) 
    qfile = open(r'E:\Netflix.Prize\data\qualifying.txt','r')
    cindex = loadCustomerRegistry()    
    qraw = qfile.readlines()
    convertedfile = open(r'E:\Netflix.Prize\conv.qualifying.txt','w')
    
    for rawline in qraw:
        line = rawline.strip()
        if line.endswith(':'): #begin movie data
            movie = int(line.replace(":",""))
            convertedfile.write(rawline)
        else: #this is a customer rating
            linedata = line.split(",")
            convertedfile.write(str(cindex[int(linedata[0])])+","+linedata[1]+"\n")            

    convertedfile.close()
    print "Qualifying set customer id's fully converted."
    
"""
    hopefully only need this once; replace the original customer id's in the probe set
"""
def convertProbe():
    startime = time()
    print "starting to convert customer id's in the probe set " + ctime(startime) 
    pfile = open(r'E:\Netflix.Prize\data\fullprobe.txt','r')
    cindex = loadCustomerRegistry()    
    praw = pfile.readlines()
    convertedfile = open(r'E:\Netflix.Prize\data\conv.fullprobe.txt','w')
    
    for rawline in praw:
        line = rawline.strip()
        if line.endswith(':'): #begin movie data
            movie = int(line.replace(":",""))
            convertedfile.write(rawline)
        else: #this is a customer rating
            linedata = line.split(",")
            convertedfile.write(str(cindex[int(linedata[0])])+","+linedata[1]+","+linedata[2]+"\n")            

    convertedfile.close()
    print "probe set customer id's fully converted."   
    
def removeProbefromMovieTraining():
    startime = time()
    print "starting to remove probe rows in the training set " + ctime(startime) 
    pmindex,pcindex = ProbeIndexLoader(probefilename)       
    
    for movie in range(1,mcount+1):
        filename = msorted_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        rfilename = mnoprobe_dir + 'mv_'+(str(movie)).zfill(7)+'.txt'
        if movie == mcount:
            print filename
        moviefile = open(filename,'r')
        rfile = open(rfilename,'w')  
        
        rawdata = moviefile.readlines()
        rfile.write(rawdata[0])
        del rawdata[0]    
        
        for rawline in rawdata:
            linedata = int(rawline.strip())
            moviedata = pmindex[movie-1]
            custid = linedata >> 3
            
            if not (custid in moviedata):
                rfile.write(rawline)
               
        if movie % 500 == 0:
            print "Training set " + ("%5.1f%%" % (100 * movie/mcount)) + " converted..."
            print str((time()-startime)//60) + " minutes have passed"
        
        moviefile.close()
        rfile.close()    
            
    print "Probe data fully removed from training set."

def ProbeIndexLoader(filename):
    movieindex, customerindex = initIndices(mcount,ccount)
            
    probefile = open(filename, 'r')
    for line in probefile:       
        probeline = line.strip()
        if probeline.endswith(':'): #begin movie data
            movie = int(line.replace(":",""))
        else: #this is a customer rating
            mpackage,cpackage,custid = lineProcesser(line,movie)            
            movieindex[movie-1] = append(movieindex[movie-1],custid)
            customerindex[custid] = append(customerindex[custid],movie)                                    
           
    return (movieindex, customerindex)

def removeProbefromCustomerTraining():
    startime = time()
    print "starting to remove probe rows in the training set " + ctime(startime) 
    pmindex,pcindex = ProbeIndexLoader(probefilename)       
    customer = -1
    for group in range(0,490000,10000):
        filename = csorted_dir + 'c_'+(str(group))+'.txt'
        rfilename = cnoprobe_dir + 'c_'+(str(group))+'.txt'
        file = open(filename,'r')
        rfile = open(rfilename,'w')
        rawdata = file.readlines()
        for rawline in rawdata:
            line = rawline.strip()           
            if line.endswith(':'): #begin movie data                
                customer = int(line.replace(":",""))
                if customer % 10000 == 0:
                    print "Probe data is " + ("%5.1f%%" % (100 * customer/ccount)) + " removed..."
                    print str((time()-startime)//60) + " minutes have passed"
                rfile.write(rawline)
            else:
                movie = int(line) >> 3
                if not (movie in pcindex[customer]):
                    rfile.write(rawline)
        rfile.close()
        file.close()    
            
    print "Probe data fully removed from training set."

"""
    loads the left lower triangular matrix of the movie correlations
"""
def loadCorrelationLTM(corrdir):             
    startime = time()
    print "starting to load correlations at " + ctime(startime) 
    corrmatrix = []

    movies = range(1,mcount+1)
    for movieid in movies:
        try:
            corrfilename = corrdir+'rho_'+(str(movieid)).zfill(7)+'.txt'
            corrfile = open(corrfilename,'r')
            rawlines = corrfile.readlines()
            correlations = [float(x.strip()) for x in rawlines]
            corrs = array(correlations, dtype=float32)
            corrmatrix.append(corrs)
            
            if movieid % 500 == 0:
                print ("%5.1f%%" % (100 * movieid/mcount)) + " of movie correlations loaded..."
                print str((time()-startime)//60) + " minutes have passed"
        except ValueError:
            print movieid    
        
    return corrmatrix

"""
    loads the left lower triangular matrix of the Fisher Z confidence intervals
"""
def loadFisherZLTM(corrdir):             
    startime = time()
    print "starting to load z-scores at " + ctime(startime) 
    corrmatrix = []

    movies = range(1,mcount+1)
    for movieid in movies:
        corrfilename = corrdir+'z_'+(str(movieid)).zfill(7)+'.txt'
        corrfile = open(corrfilename,'r')
        rawlines = corrfile.readlines()
        correlations = [float(x.strip()) for x in rawlines]
        corrs = array(correlations, dtype=float32)
        corrmatrix.append(corrs)
        
        if movieid % 500 == 0:
            print ("%5.1f%%" % (100 * movieid/mcount)) + " of movie z-scores loaded..."
            print str((time()-startime)//60) + " minutes have passed"    
    
    return corrmatrix