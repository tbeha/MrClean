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

logwriter(log,"Cron Test")

logclose(log)
