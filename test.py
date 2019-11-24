from datetime import datetime

def logwriter(f, text):
    f.write(str(datetime.today()) +": "+text+" \n")
    
def logopen(filename):
    f = open(filename,"a")
    f.write(str(datetime.today())+": Logfile opened \n")
    return f

def logclose(f):
    f.write(str(datetime.today())+": Logfile closed \n")
    f.close()

today=datetime.today()
logfile="test."+str(datetime.today())[0:10]+".log"
log=logopen(logfile)

prefix='morph-'
files=["morph-vm001","vm002"]

for x in files:    
    if(x.find(prefix) > -1):
        logwriter(log,"Found prefix in "+x)

    

logwriter(log,"Cron Test")

logclose(log)
