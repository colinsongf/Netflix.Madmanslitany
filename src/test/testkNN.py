from learning.kNN import *
from data.Loader import customerArrayBinarySearch
import cProfile

def main1():
    rv = 0
    for i in range(0,10000):
        m1 = [(101,1),(102,3),(103,5),(104,6),(105,1),(106,3),(107,2)]
        m1 = [(x[0] << 3) | x[1] for x in m1]
        m2 = [(101,5),(102,4),(103,3),(104,2),(105,4),(106,4),(107,1)]
        m2 = [(x[0] << 3) | x[1] for x in m2]
        mi = array('L')
        for i in m1:
            mi.append(i)
        mj = array('L')
        for j in m2:
            mj.append(j)                
        rv = moviesimilarity_Pearson(mi,mj)
    print rv

cProfile.run('main1()')