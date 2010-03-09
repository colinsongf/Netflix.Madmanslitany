from __future__ import division
from Loader import *
from numpy import *
from constants import *

def customerOffsetProbe():
    cindex = SortedProbelessUserLoader()
    globalsum = 0
    ratingcount = 0
    userstats = empty((ccount))
    
    for userid in range(0,ccount):
        userdata = cindex[userid]
        for datum in userdata:
            rating = datum & 0x7
            globalsum += float(rating) - global_movie_avg_probe
            ratingcount += 1
    
    globaloffset = globalsum/ratingcount
    
    print globaloffset
    
    return globaloffset

def movieAverageProbe():
    mindex = SortedProbelessMovieLoader()
    globalsum = 0
    ratingcount = 0
    moviestats = empty((mcount))
    
    for movieid in range(1,mcount+1):
        moviedata = mindex[movieid-1]
        for datum in moviedata:
            rating = datum & 0x7
            globalsum += rating
            ratingcount += 1
    
    globalavg = globalsum/ratingcount
    
    print globalavg
    
    return globalavg

    
customerOffsetProbe()