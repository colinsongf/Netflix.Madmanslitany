from data.constants import *
from data.Loader import *
from data.Serializer import *

def test1():
    sentinel = 1
    
    mindex,cindex = deserializeSortedTrainingSet()
    cregistry = loadCustomerRegistry()    
   
    for mid in (10,10000,13568,500,17000):
        filename = train_dir + 'mv_'+(str(mid)).zfill(7)+'.txt'
        file = open(filename,'r')
        rawdata = file.readlines()
        del rawdata[0]
        sourcedata = []
        for line in rawdata:
            rawlist = line.split(",")
            sourcedata.append((cregistry[int(rawlist[0])],int(rawlist[1])))
    
        mdata = mindex[mid-1]    
        mdata = [(x >> 3,x & 0x7) for x in mdata]
        
        for datum in sourcedata:
            if not (datum in mdata):
                print datum
                sentinel = 0
        
        if sentinel:
            print "test 1 succeeded!"
        else:
            print "test 1 FAILED!"
    
test1()   