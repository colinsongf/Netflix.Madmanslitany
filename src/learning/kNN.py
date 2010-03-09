from __future__ import division
import os
import cProfile
from math import sqrt
from heapq import *
from array import *
from data.Loader import SortedTrainingLoader
from data.Loader import mcount
from data.Loader import pcount
from time import *
from math import log
from math import exp
from correlation import pearson
from fisher import fisher
from overlap import overlap_count

"""
    fisher functions from http://www.netflixprize.com/community/viewtopic.php?id=697
"""
def fisher_z_transform(x):    
    #The Fisher z' transform
    z = .5*( log((1+x)/(1-x)) )
    return z

def inverse_fisher_z_transform(x):    
    #The Fisher z' inverse transform
    zi = (exp(2*x)-1)/(exp(2*x)+1)
    return zi
    
def fisher_sigma(n):    
    #The standard deviation in Fisher's space:
    sigma = 1/(sqrt(n-3))    
    return sigma

def l_confidence_correlation(rho,n):
    print "entering l confidence correlation with rho of " + str(rho)
    left_r_score = 1.0
    if not (rho==1.0 or rho==1):
        sigma = fisher_sigma(n)    
        CONF_LEVEL = 1.96 # this corresponds to 95% confidence
        z = fisher_z_transform(rho)
        left_r_score = inverse_fisher_z_transform( z - sigma*CONF_LEVEL )
    return left_r_score    

def cached_Similarity(correlations,i,j):
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

"""
    the similarity between two customers
    basing this on Pearson correlation coefficient
    this has been re-implemented as C extension correlation
"""
def moviesimilarity_Pearson(mi,mj):
    leni = len(mi)
    lenj = len(mj)

    sumxy = 0
    sumx = 0
    sumy=0
    sumx2 = 0
    sumy2 = 0
    n = 0
    i = 0
    j = 0

    while i<leni and j<lenj:
        Ci = mi[i]>>3
        Cj = mj[j]>>3
        if Ci == Cj:
            xi = mi[i] & 0x7
            yi = mj[j] & 0x7
            sumx+=xi
            sumy+=yi
            sumxy+=xi*yi
            sumx2+=xi**2
            sumy2+=yi**2            
            i+=1
            j+=1
            n+=1
        elif Ci > Cj:
            j += 1
        else:
            i += 1 

    if sumx2==sumy2 and sumx==sumy:
        print "fully correlated!"
        return 1.0
    else:
        denominator = 0
        try:
            denominator = sqrt(abs(n*sumx2-sumx**2))*sqrt(abs(n*sumy2-sumy**2))
        except ValueError:
            print "n = " + str(n)
            print "sumx2 = " + str(sumx2)
            print "sumx = " + str(sumx)
            print "sumy2 = " +str(sumy2)
            print "sumy = " +str(sumy)
            print "first half =" + str(n*sumx2-sumx**2)
            print "second half =" + str(n*sumy2-sumy**2)
            print "whole = "+str((n*sumx2-sumx**2)*(n*sumy2-sumy**2))
        #correlation is undefined if one of the deviations is zero
        if denominator!=0:
            numerator = n*sumxy-sumx*sumy       
            correlation = numerator/denominator        
            return correlation
        else:
            return 0
 

"""
    distance-weighted kNN
"""
def kNNPrediction_Distance_Weighted(similarity,targetid,customerdata,mindex,customerid,k,correlations):
    neighbors = []  #list of customer id's
    nn = [] #list of nearest neighbors
    
    for movieid in customerdata:        
        #score = similarity(mindex[targetid-1],mindex[(movieid >> 3)-1])
        score = cached_Similarity(correlations,targetid-1,(movieid >> 3)-1)
        if score>0.0001:
            heappush(neighbors,(score,movieid & 0x7))        

    i = 0
    summation = 0
    w = 0
    
    while neighbors and i<k:
        n = heappop(neighbors)
        summation+=n[0]**2*n[1]
        w+=n[0]**2
        i+=1

    prating = 3
    if w > 0:
        prating = summation/w        
            
    return prating

"""
    kNN prediction
"""
def kNNPrediction(similarity,targetid,customerdata,mindex,customerid,k,correlations):
    neighbors = []  #list of customer id's
    nn = [] #list of nearest neighbors
    
    for movieid in customerdata:        
        #score = similarity(mindex[targetid-1],mindex[(movieid >> 3)-1])
        score = cached_Similarity(correlations,targetid-1,(movieid >> 3)-1)
        if score!=0:
            heappush(neighbors,(score,movieid & 0x7,(movieid >> 3)-1))        

    i = 0
    summation = 0
    w = 0
    
    while neighbors and i<k:
        n = heappop(neighbors)
        oc = overlap_count(mindex[targetid-1],mindex[n[2]])
        wi = 0
        if(oc>0):
            wi = log(oc)
        summation+=wi*n[1]
        w+=wi
        i+=1

    prating = 3
    if w > 0:
        prating = summation/w        
            
    return prating

"""
    function to actually run this algorithm
"""
def run(mindex,cindex,qorder,qset,predictions,progress,k,correlations):                  
    start = 1    
    startime = time()
    print "starting kNN classification at " + ctime(startime)
    counter = 0
    pcounter = 0
    masterpcounter = 0
    predlist = []
    for movieid in qorder:
        predlist.append(str(movieid)+":\n")        
        moviepredictions = [str(kNNPrediction(pearson,movieid,cindex[customerid],mindex,customerid,k,correlations))+"\n" for customerid in qset[movieid-1]]
        pcounter += len(moviepredictions)
        counter += 1            
        predlist.extend(moviepredictions)
        if movieid == qorder[len(qorder)-1] or counter % 20 == 0:
            predictions.writelines(predlist)
            predictions.flush()
            predlist = []          
            progress.write(str(movieid)+"\n")
            progress.flush()
            print "Writing results at " + ctime(time())
            print "Analyzed " + str(counter) + " movies..."
            print "Generated a total of " + str(pcounter) + " predictions..."
            print "Classification is " + ("%5.1f%%" % (100 * pcounter/pcount)) + " complete."
            print str((time()-startime)//60) + " minutes have passed"