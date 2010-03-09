from learning.overlap import overlap_count
from numpy import *
import cProfile


def test2():           
    m1 = [(99,1),(101,1),(102,3),(104,5),(105,4),(106,1),(107,3),(108,2)]
    m1 = [(x[0] << 3) | x[1] for x in m1]
    m2 = [(99,1),(101,1),(102,3),(104,5),(105,4),(106,1),(107,3),(108,2)]
    m2 = [(x[0] << 3) | x[1] for x in m2]
               
    mi = array(m1)
    mj = array(m2)
    rv = overlap_count(mi,mj)
    
    if rv!=8:
        print "Test 2 FAILED, n was " + str(rv) + " instead of 8."
    else:
        print "Test 2 passed!"


def test1():           
    m1 = [(99,1),(101,1),(102,3),(104,5),(105,4),(106,1),(107,3),(108,2)]
    m1 = [(x[0] << 3) | x[1] for x in m1]
    m2 = [(99,1),(101,1),(102,3),(104,5),(105,4),(106,1),(107,3),(108,2)]
    m2 = [(x[0] << 3) | x[1] for x in m2]
               
    mi = array(m1)
    mj = array(m2)
    rv = overlap_count(mi,mj)
    
    if rv!=8:
        print "Test 1 FAILED, n was " + str(rv) + " instead of 8."
    else:
        print "Test 1 passed!"
    
    
test1()
test2()