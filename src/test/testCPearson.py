from numpy import *
from learning.correlation import *
import cProfile

def test3():
    rv = 0
    
    m1 = [(99,5),(101,4),(102,4),(104,4),(105,2),(106,3),(107,2)]
    m1 = [(x[0] << 3) | x[1] for x in m1]
    m2 = [(99,5),(101,4),(102,3),(104,4),(105,4),(106,4),(107,1)]
    m2 = [(x[0] << 3) | x[1] for x in m2]
       
    mi = array(m1)
    mj = array(m2)
    fn = pearson
    rv = fn(mi,mj)
    if rv - 0.61509 > 0.001:
        print "Test 3 FAILED!"
    else:
        print "Test 3 passed!"
    print rv

def test2():
    rv = 0
    
    m1 = [(99,1),(101,1),(102,3),(104,5),(105,4),(106,1),(107,3),(108,2)]
    m1 = [(x[0] << 3) | x[1] for x in m1]
    m2 = [(99,1),(101,1),(102,3),(104,5),(105,4),(106,1),(107,3),(108,2)]
    m2 = [(x[0] << 3) | x[1] for x in m2]
       
    mi = array(m1)
    mj = array(m2)
    fn = pearson
    rv = fn(mi,mj)
    if rv - 1 > 0.001:
        print "Test 2 FAILED!"
    else:
        print "Test 2 passed!"
    print rv

def test1():
    rv = 0
    
    m1 = [(99,1),(101,1),(102,3),(104,5),(105,4),(106,1),(107,3),(108,2)]
    m1 = [(x[0] << 3) | x[1] for x in m1]
    m2 = [(100,3),(101,5),(102,4),(103,2),(104,3),(105,2),(106,4),(107,4),(108,1),(150,3)]
    m2 = [(x[0] << 3) | x[1] for x in m2]
       
    mi = array(m1)
    mj = array(m2)
    fn = pearson
    rv = fn(mi,mj)
    if rv + 0.35748 > 0.001:
        print "Test 1 FAILED!"
    else:
        print "Test 1 passed!"
    print rv

def testsuite():
    test1()
    test2()
    test3()

testsuite()