
# coding: utf-8

# In[ ]:

def checkSorted(contacts):
    for i in range(1,len(contacts)):
        if contacts[i][0] < contacts[i-1][0]:
            return 1
        elif contacts[i][0] == contacts[i-1][0]:
            if contacts[i][1] < contacts[i-1][1]:
                return 1
            elif contacts[i][1] == contacts[i-1][1]:
                if contacts[i][2] < contacts[i-1][2]:
                    return 1
                elif contacts[i][2] == contacts[i-1][2]:
                    if contacts[i][3] < contacts[i-1][3]:
                        return 1
                    elif contacts[i][3] == contacts[i-1][3]:
                        if contacts[i][4] < contacts[i-1][4]:
                            return 1
                        elif contacts[i][4] == contacts[i-1][4]:
                            if contacts[i][5] < contacts[i-1][5]:
                                return 1
        elif contacts[i-1][0] > contacts[i-1][3]:
            return 2
        elif contacts[i-1][0] == contacts[i-1][3]:
            if contacts[i-1][1] > contacts[i-1][4]:
                return 2
            elif contacts[i-1][1] == contacts[i-1][4]:
                if contacts[i-1][2] > contacts[i-1][5]:
                    return 2
    return 0


# In[ ]:

def checkSortedBed(bed):
    for i in range(1,len(bed)):
        if bed[i][0] < bed[i-1][0]:
            return False
        elif bed[i][0] == bed[i-1][0]:
            if bed[i][1] < bed[i-1][1]:
                return False
            elif bed[i][1] == bed[i-1][1]:
                if bed[i][2] < bed[i-1][2]:
                    return False
    return True


# In[ ]:

def processFile(FILENAME):
    header=""
    processedFile=[]
    for line in open(FILENAME,"r"):
        if line=="\n":
            continue
        if line[0]=="#":
            header+=line.strip()+"\n"
        else:
            x=line.strip().split()
            if len(x)<6:
                print("Missing one of the required 6 columns")
                print line
                exit()
            else:
                processedFile.append([x[0],int(x[1]),int(x[2]),x[3],int(x[4]),int(x[5]), x[6:]])
    return header[:-1],processedFile


# In[ ]:

def processStdin():
    import sys
    header=""
    processedFile=[]
    for line in sys.stdin:
        if line=="\n":
            continue
        if line[0]=="#":
            header+=line.strip()+"\n"
        else:
            x=line.strip().split()
            if len(x)<6:
                print("Missing one of the required 6 columns")
                exit()
            else:
                processedFile.append([x[0],int(x[1]),int(x[2]),x[3],int(x[4]),int(x[5]), x[6:]])
    return header[:-1],processedFile


# In[ ]:

def processBedFile(fileName):
    bed={}
    header=""
    with open(fileName,"r") as f:
        for line in f:
            if line=="\n":
                continue
            if line[0]=="#":
                header+=line.strip()+"\n"
            else:
                line=line.strip().split()
                if line[0] in bed:
                    bed[line[0]].append([int(line[1]),int(line[2]),line[3:]])
                else:
                    bed[line[0]]=[[int(line[1]),int(line[2]),line[3:]]]
    return header[:-1],bed


# In[ ]:

def processStdinBed():
    import sys
    bed={}
    header=""
    for line in sys.stdin:
        if line=="\n":
            continue
        if line[0]=="#":
            header+=line.strip()+"\n"
        else:
            line=line.strip().split()
            if line[0] in bed:
                bed[line[0]].append([int(line[1]),int(line[2]),line[3:]])
            else:
                bed[line[0]]=[[int(line[1]),int(line[2]),line[3:]]]
    return header[:-1],bed


