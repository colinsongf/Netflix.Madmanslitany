from __future__ import division
from math import sqrt
from constants import probefilename

def main():
    realfile = open(probefilename,'r')
    predfile = open(r'C:\Netflix\kNN\probe\predictions.txt','r')
    
    real = realfile.readlines()
    predictions = predfile.readlines()

    numvals = 0
    sumsquares = 0
        
    for i in range(0,len(real)):
        rline = real[i].strip()
        pline = predictions[i].strip()
        if not rline.endswith(':'): #begin movie data
            rdata = rline.split(",")
            rrating = float(rdata[1])
            prating = float(pline)
            delta = rrating - prating
            numvals += 1
            sumsquares += delta**2

    rmse = sqrt(sumsquares/numvals)

    print "RMSE: " + str(rmse)
    
main()    