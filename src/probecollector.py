import os

def padzero(s):
    return(('0' * (7-len(s))) + s)

def main():
    probefile = open(r'C:\Netflix.Prize\data\probe.txt', 'r')
    os.remove(r'C:\Netflix.Prize\data\fullprobe.txt')
    fullprobefile = open(r'C:\Netflix.Prize\data\fullprobe.txt','w')
    
    probe = {}
    movie = 1
    
    for rawline in probefile:
        line  = rawline.strip()
        if line.endswith(":"):
            movie = int(line.replace(":",""))
            if probe.has_key(movie)==False:
                probe[movie] = {}
                """if movie>10000:
                break"""    
        else:
            probe[movie][int(line)]=(-1,"")
    
    print "Finished reading probe.txt"
            
    for movie in probe.keys():
        moviefilename = "mv_"+padzero(str(movie))+".txt"
        moviefile = open('C:\\Netflix.Prize\\data\\training_set\\training_set\\'+moviefilename,'r')
        for rawline in moviefile:
            line = rawline.strip()
            if line.endswith(":")==False:
                ratinglist = line.split(",")
                if(probe[movie].has_key(int(ratinglist[0]))):
                    probe[movie][int(ratinglist[0])]=(int(ratinglist[1]),ratinglist[2])
    
    print "Finished processing mv_ files"
    
    testpassed = True
    
    for movie in probe.keys():
        for customer in probe[movie].keys():
            ratingtuple=probe[movie][customer]
            if ratingtuple[0]==-1 or ratingtuple[1]=="":
                testpassed = False
    
    if testpassed:
        print "Success!  Now writing results to new file..."
        for movie in probe.keys():
            fullprobefile.write(str(movie)+":"+"\n")
            for customer in probe[movie].keys():
                ratingtuple=probe[movie][customer]
                fullprobefile.write(str(customer)+","+str(ratingtuple[0])+","+ratingtuple[1]+"\n")       
    else:
        print "FAILURE!"

main()        