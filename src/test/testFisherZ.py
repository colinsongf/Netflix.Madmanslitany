from learning.fisher import fisher
from learning.correlation import pearson
from data.Loader import SortedProbelessMovieLoader
from data.Loader import loadCorrelationLTM
from data.constants import *
from learning.kNN import moviesimilarity_Pearson
from learning.kNN import l_confidence_correlation
from numpy import *
from time import *
from learning.overlap import overlap_count
    
def test1():
    mindex = SortedProbelessMovieLoader()
    prefix = 'D:\\Netflix.Prize\\data\\probe.fisherz.rlimit\\z_'
    suffix = '.txt'
    
    startime = time()
    print "starting to calculate fisher z scores at " + ctime(startime)

    movieid = 27
    cols = range(0, movieid)
    r_scores = [(str(moviesimilarity_Pearson(mindex[movieid-1],mindex[x])) + "\n") for x in cols]
    z_scores = [str(l_confidence_correlation(moviesimilarity_Pearson(mindex[movieid-1],mindex[x]), overlap_count(mindex[movieid - 1], mindex[x]))) + "\n" for x in cols]
    #z_scores = [str(fisher(x, overlap_count(mindex[movieid - 1], mindex[x]))[1]) + "\n" for x in z_scores]    
    print z_scores
    
test1()