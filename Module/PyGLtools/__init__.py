
# coding: utf-8

# In[ ]:

def _checkSorted(contacts):
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

def _processBedFile(FILENAME):
    bed={}
    header=""
    for line in FILENAME.split("\n"):
        if line[0]=="#":
            header+=line.strip()+"\n"
        else:
            line=line.strip().split()
            if line[0] in bed:
                bed[line[0]].append([int(line[1]),int(line[2]),line[3:]])
            else:
                bed[line[0]]=[[int(line[1]),int(line[2]),line[3:]]]
    return header,bed


# In[ ]:

def _processFile(FILENAME):
    header=""
    processedFile=[]
    for line in FILENAME.split("\n"):
        if line[0]=="#":
            header+=line+"\n"
        else:
            x=line.split()
            if len(x)<6:
                return ("Missing one of the required 6 columns")
            else:
                processedFile.append([x[0],int(x[1]),int(x[2]),x[3],int(x[4]),int(x[5]), x[6:]])
    return header[:-2],processedFile


# In[ ]:

def sort(contacts):
    header,contacts=_processFile(contacts)
    delim="\t"
    contacts=sorted(contacts,key=lambda x:(x[0],int(x[1]),int(x[2]),x[3],int(x[4]),int(x[5])))
    contacts=[delim.join([str(y) for y in x[:6]])+delim+delim.join([str(y) for y in x[6]]) for x in contacts]
    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(contacts)
    
    return output


# In[ ]:

def _processCommands(contacts,cols,commands,dashDelim):
    if len(cols)>0:
        for i in range(len(contacts)):
            newAnnot=[]
            for ind in range(len(cols)):
                if type(contacts[i][6][0])!=list and cols[ind]!=0:
                    newAnnot.append(operation([contacts[i][6][cols[ind]-6]],commands[ind],dashDelim))
                else:
                    newAnnot.append(operation(contacts[i][6][ind],commands[ind],dashDelim))

            contacts[i][6]=newAnnot
    else:
        contacts=[x[:6] for x in contacts]
    return contacts


# In[ ]:

def _processRead(name,chrom,start,length,cigar,flipped):
    Name=name
    Chrom=chrom
    if flipped:
        End=start
        Start=End-length
    else:
        Start=start
        End=start+length
    cigarSplit=[]
    temp=""
    for c in cigar:
        temp+=c
        if not str.isalpha(c):
            cigarSplit.append(c)
            temp=""
            
    for cc in cigarSplit:
        if (cc[-1] == 'M' or cc[-1] == 'D'):
            End+=int(cc[:-1])
        elif cc[-1] == 'I':
            End-=-int(cc[:-1])
    
    return [Name,Chrom,Start,End]


# In[ ]:

def _processSubtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,whichBin):
    if whichBin==1:
        if startA1 < startB:
            if endA1<endB:
                return [[chrA1,startA1,startB,chrA2,startA2,endA2,Aannots]]
            else:
                return [[chrA1,startA1,startB,chrA2,startA2,endA2,Aannots],[chrA1,endB,endA1,chrA2,startA2,endA2,Aannots]]
        else:
            if endA1<endB:
                return [[]]
            else:
                return [[chrA1,startB,endA1,chrA2,startA2,endA2,Aannots]]
    elif whichBin==2:
        if startA2 < startB:
            if endA2<endB:
                return [[chrA1,startA1,endA1,chrA2,startA2,startB,Aannots]]
            else:
                return [[chrA1,startA1,endA1,chrA2,startA2,startB,Aannots],[chrA1,startA1,endA1,chrA2,endB,endA2,Aannots]]
        else:
            if endA2<endB:
                return [[]]
            else:
                return [[chrA1,startA1,endA1,chrA2,startB,endA2,Aannots]]


# In[ ]:

def _createHeader(originalHeader,cols,commands,oldHeaderIsUsable):
    header="#chrA\tstartA\tendA\tchrB\tstartB\tendB\t"
    for i in range(len(cols)):
        if oldHeaderIsUsable:
            if commands[i]=="count" and cols[i]==0:
                header+="count\t"
            else:
                header+=commands[i]+"_of_"+originalHeader[cols[i]]+"\t"
        else:
            if commands[i]=="count" and cols[i]==0:
                header+="count\t"
            else:
                header+=commands[i]+"_of_"+str(cols[i])+"\t"
    return header


# In[ ]:

def _operation(operatedOnList,operation,delim):
    if operation=="sum":
        return sum([float(x) for x in operatedOnList])
    elif operation=="min":
        return min([float(x) for x in operatedOnList])
    elif operation=="max":
        return max([float(x) for x in operatedOnList])
    elif operation=="absmin":
        absmin=-1
        for x in operatedOnList:
            if abs(x) < absmin or absmin==-1:
                absmin=x
        return absmin
    elif operation=="absmax":
        absmax=-1
        for x in operatedOnList:
            if abs(x) > absmax or absmax==-1:
                absmax=x
        return absmax
    elif operation=="mean":
        return sum([float(x) for x in operatedOnList])/len(operatedOnList)
    elif operation=="median":
        operatedOnList==sorted([float(x) for x in operatedOnList])
        if len(operatedOnList)%2==0:
            return (operatedOnList[(len(operatedOnList))/2]+operatedOnList[((len(operatedOnList))/2)-1])/2
        else:
            return operatedOnList[(len(operatedOnList)-1)/2]
    elif operation=="collapse":
        return delim.join([str(x) for x in operatedOnList])
    elif operation=="distinct":
        return delim.join([str(x) for x in set(operatedOnList)])
    elif operation=="count":
        return max(1,len(operatedOnList))
    elif operation=="count_distinct":
        return (len(list(set(operatedOnList))))


# In[ ]:

def browser(contacts,trackName="pgltrack",nameCol=-1,scoreCol=-1,pCol=-1,qCol=-1):
    """Format contacts for viewing in the UCSC Genome Browser"""
    
    _,contacts=_processFile(contacts)
    res=[]
    i=-1
    for contact in contacts:
        i+=1
        if contact[0]!=contact[3]:
            continue
        chrom=contact[0]
        start=str(contact[1])
        end=str(contact[5])
        if nameCol!=-1:
            name=contact[6][nameCol-6]
        else:
            name="chr:"+str(contact[1])+".."+str(contact[2])+"-chr:"+str(contact[4])+".."+str(contact[5])
        if scoreCol!=-1:
            score=contact[6][scoreCol-6]
        else:
            score="1000"
        strand="."
        thickStart="0"
        thickEnd="0"
        rgb="0"
        blockCount="2"
        blockSizes=str(contact[2]-contact[1])+","+str(contact[5]-contact[4])
        blockStarts="0,"+str(contact[4]-contact[1])
        signalValue="0"
        if pCol!=-1:
            pValue=contact[6][pCol-6]
        else:
            pValue="0"
        if qCol!=-1:
            qValue=contact[6][qCol-6]
        else:
            qValue="0"
        
        res.append("\t".join([chrom,start,end,name,score,strand,thickStart,thickEnd,rgb,blockCount,blockSizes,blockStarts,signalValue,pValue,qValue]))
        
    output="track name="+trackName+" type=gappedPeak"
    output+="\n".join(res)
    return output


# In[ ]:

def closest(contactsA,contactsB):
    """Find the closest entry from contactsB for each entry in contactsA"""
    
    header,contactsA=_processFile(contactsA)
    _,contactsB=_processFile(contactsB)
    
     #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    newPeaks=[]
    #compare file 2 to file 1, meaning advance file 2 first
    for k in range(len(contactsB)):
        distance=-1
        closestFeature=-1
        for i in range(len(contactsA)):
            
            chrA1=contactsA[i][0]
            startA1=contactsA[i][1]
            endA1=contactsA[i][2]
            chrA2=contactsA[i][3]
            startA2=contactsA[i][4]
            endA2=contactsA[i][5]

            chrB1=contactsB[k][0]
            startB1=contactsB[k][1]
            endB1=contactsB[k][2]
            chrB2=contactsB[k][3]
            startB2=contactsB[k][4]
            endB2=contactsB[k][5]

            if chrA1!=chrB1 or chrA2!=chrB2:
                continue
            else:
                if startA1 < startB1 and endA1 < startB1:
                    bin1Dist=startB1-endA1
                elif startB1 < startA1 and endB1 < startA1:
                    bin1Dist=startA1-endB1
                else:
                    bin1Dist=0
                if startA2 < startB2 and endA2 < startB2:
                    bin2Dist=startB2-endA2
                elif startB2 < startA2 and endB2 < startA2:
                    bin2Dist=startA2-endB2
                else:
                    bin2Dist=0
                    
                if bin1Dist+bin2Dist < distance or distance==-1:
                    distance=bin1Dist+bin2Dist
                    closestFeature=i

        if closestFeature!=-1:
            newPeaks.append([contactsB[k][:6],contactsA[closestFeature][:6],distance])
        else:
            newPeaks.append([contactsB[k][:6],[".",".",".",".",".","."],"."])
    delim="\t"
    newPeaks = [delim.join([delim.join([str(y) for y in x[0]]),delim.join([str(y) for y in x[1]]),str(x[2])]) for x in newPeaks]
    output= "\t".join(["#fileA_chrA","fileA_startA","fileA_stopA","fileA_chrB","fileA_startB","fileA_stopB",
                 "fileB_chrA","fileB_startA","fileB_stopA","fileB_chrB","fileB_startB","fileB_stopB","Distance"])
    output+="\n".join(newPeaks)
    
    return output


# In[ ]:

def closest1D(contactsA,bedB,dashBA=False):
    """find the closest entry in bedB for each entry in contactsA"""
    
    header,contactsA=_processFile(contactsA)
    _,bedB=_processBedFile(bedB)
    
     #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    newPeaks=[]
    #compare file 2 to file 1, meaning advance file 2 first
    for i in range(len(contactsA)):
        if dashBA:
            Anch1Distance=-1
            Anch2Distance=-1
            Anch1Feat=-1
            Anch2Feat=-1
        else:
            distance=-1
        
        closestFeature=-1

        chrA1=contactsA[i][0]
        startA1=contactsA[i][1]
        endA1=contactsA[i][2]
        chrA2=contactsA[i][3]
        startA2=contactsA[i][4]
        endA2=contactsA[i][5]

        if chrA1==chrA2:
            if chrA1 in bedB:
                for k in range(len(bedB[chrA1])):
                    chrB=chrA1
                    startB=bedB[chrA1][k][0]+1
                    endB=bedB[chrA1][k][1]
                    if startA1 < startB and endA1 < startB:
                        bin1Dist=startB-endA1
                    elif startB < startA1 and endB < startA1:
                        bin1Dist=startA1-endB
                    else:
                        bin1Dist=0
                    if startA2 < startB and endA2 < startB:
                        bin2Dist=startB-endA2
                    elif startB < startA2 and endB < startA2:
                        bin2Dist=startA2-endB
                    else:
                        bin2Dist=0

                    minDist=min(bin1Dist,bin2Dist)
                    
                    
                    if not dashBA:
                        if minDist < distance or distance==-1:
                            distance=minDist
                            closestFeature=(chrB,k)
                    else:
                        if bin1Dist < Anch1Distance or Anch1Distance==-1:
                            Anch1Distance=bin1Dist
                            Anch1Feat=(chrB,k)
                        if bin2Dist < Anch2Distance or Anch2Distance==-1:
                            Anch2Distance=bin2Dist
                            Anch2Feat=(chrB,k)


        else:
            if chrA1 in bedB:
                for k in range(len(bedB[chrA1])):
                    chrB=chrA1
                    startB=bedB[chrA1][k][0]+1
                    endB=bedB[chrA1][k][1]
                    if startA1 < startB and endA1 < startB:
                        bin1Dist=startB-endA1
                    elif startB < startA1 and endB < startA1:
                        bin1Dist=startA1-endB
                    else:
                        bin1Dist=0
                        
                    if not dashBA:
                        if bin1Dist < distance or distance==-1:
                            distance=bin1Dist
                            closestFeature=(chrB,k)
                    else:
                        if bin1Dist < Anch1Distance or Anch1Distance==-1:
                            Anch1Distance=bin1Dist
                            Anch1Feat=(chrB,k)
            if chrA2 in bedB:
                for k in range(len(bedB[chrA2])):
                        chrB=chrA2
                        startB=bedB[chrA1][k][0]+1
                        endB=bedB[chrA1][k][1]
                        if startA2 < startB and endA2 < startB:
                            bin2Dist=startB-endA2
                        elif startB < startA2 and endB < startA2:
                            bin2Dist=startA2-endB
                        else:
                            bin2Dist=0
                        if not dashBA:
                            if bin2Dist < distance or distance==-1:
                                distance=bin2Dist
                                closestFeature=(chrB,k)
                        else:
                            if bin2Dist < Anch2Distance or Anch2Distance==-1:
                                Anch2Distance=bin2Dist
                                Anch2Feat=(chrB,k)

        if not dashBA:
            if closestFeature!=-1:
                entry=[closestFeature[0]]
                entry.extend(bedB[closestFeature[0]][closestFeature[1]][:2])
                entry.append(str(distance))
                newPeaks.append([contactsA[i][:6],entry])
            else:
                newPeaks.append([contactsA[i][:6],[".",".",".","."]])
        else:
            entry=[]
            if Anch1Feat!=-1:
                entry=[Anch1Feat[0]]
                entry.extend(bedB[Anch1Feat[0]][Anch1Feat[1]][:2])
                entry.append(str(Anch1Distance))
            else:
                entry.extend([".",".",".","."])
            if Anch2Feat!=-1:
                entry.append(Anch2Feat[0])
                entry.extend(bedB[Anch2Feat[0]][Anch2Feat[1]][:2])
                entry.append(str(Anch2Distance))
            else:
                entry.extend([".",".",".","."])
            newPeaks.append([contactsA[i][:6],entry])
    
    delim="\t"       

    newPeaks=[delim.join([str(y) for y in x[0]])+delim+delim.join([str(y) for y in x[-1]]) for x in newPeaks]
    
    if not dashBA:
        output= "\t".join(["#chrA","startA","stopA","chrB","startB","stopB","closestChr","closestStart","closestStop","distance"])+"\n"
    else:
        output= "\t".join(["#chrA","startA","stopA","chrB","startB","stopB","closestAChr","closestAStart","closestAStop",
                         "distanceToA","closestBChr","closestBStart","closestBStop","distanceToB"])+"\n"

    output+="\n".join(newPeaks)
    
    return output


# In[ ]:

def conveRt(contacts,countCol=-1,pCol=-1,qCol=-1):
    """Concert contacts to a format for use with the GenomicInteractions package."""
    header,contacts=_processFile(contacts)
    res=[]
    i=-1
    for contact in contacts:
        if countCol!=-1:
            count=contact[6][countCol-6]
        else:
            count="0"
        if pCol!=-1:
            pValue=contact[6][pCol-6]
        else:
            pValue="0"
        if qCol!=-1:
            qValue=contact[6][qCol-6]
        else:
            qValue="0"
        
        res.append("\t".join([contact[0],str(contact[1]),str(contact[2]),contact[3],str(contact[4]),str(contact[5]),count,pValue,qValue]))
    delim="\t" 
    
    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(res)
    
    return output


# In[ ]:

def coverage(contactsA,contactsB,dashZ=False):
    """find the number of entries in contactsB that overlap entries in contactsA"""
    #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    
    header,contactsA=_processFile(contactsA)

    if _checkSorted(contactsA)==1:
        return ("contactsA is not sorted.  Please use PyGLtools.sort(contactsA)")

    elif _checkSorted(contactsA)==2:
        return ("contactsA is not a pgl file.  Please use PyGLtools.formatbedpe(contactsA)")

        
    _,contactsB=_processFile(contactsB)

    if _checkSorted(contactsB)==1:
        return ("contactsB is not sorted.  Please use PyGLtools.sort(contactsB)")
    elif _checkSorted(contactsB)==2:
        return ("contactsB is not a pgl file.  Please use PyGLtools.formatbedpe(contactsB)")

    
    i=0
    k=0
    restartK=-1
    newPeaks=[]
    maximalRestart=0
    #compare file 2 to file 1, meaning advance file 2 first
    while i<len(contactsA) and k<len(contactsB):
            
        chrA1=contactsA[i][0]
        startA1=contactsA[i][1]
        endA1=contactsA[i][2]
        chrA2=contactsA[i][3]
        startA2=contactsA[i][4]
        endA2=contactsA[i][5]
        Aannotations=contactsA[i][6]
        
        if k==-1:
            k=0
        chrB1=contactsB[k][0]
        startB1=contactsB[k][1]
        endB1=contactsB[k][2]
        chrB2=contactsB[k][3]
        startB2=contactsB[k][4]
        endB2=contactsB[k][5]

        if endB1 > maximalRestart:
            maximalRestart=endB1
        
        #check chromosome on first bin
        if chrA1<chrB1:
            i+=1
            k=restartK
        elif chrA1>chrB1:
            k+=1
            restartK=k
            continue
        else:
            #on the same chromosome
            #we have a two options: first bins overlap or they dont.

            if startA1 < startB1 and endA1 < startB1:
                i+=1
                k=restartK
                continue
            elif startB1 < startA1 and endB1 < startA1:
                if maximalRestart<=startA1: #should always ==, < is present for my sanity
                    restartK=k
                k+=1
                continue

            else:
            #the bins overlap in some way.  Now we advance to bin2
                if restartK==-1:
                    restartK=k
                if chrA2!=chrB2:
                    k+=1
                    continue
                    

            #on the same chromosome
            #we have a two options: second bins overlap or they dont.

               if startA2 < startB2 and endA2 < startB2:
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1

                elif startB2 < startA2 and endB2 < startA2:
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1 

            #bins overlap
                else:
                    newPeaks.append([contactsA[i][:6]])
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1
    delim="\t"            
    newPeaks=[delim.join([str(y) for y in x[0]])for x in newPeaks]
    Counts={}
    for r in newPeaks:
        if r in Counts:
            Counts[r]+=1
        else:
            Counts[r]=1
    
    if not dashZ:
        newPeaks=[x+"\t"+str(Counts[x]-1) for x in list(set(newPeaks)) if Counts[x]-1>=1]
    else:
        newPeaks=[x+"\t"+str(Counts[x]-1) for x in list(set(newPeaks))]

    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(newPeaks)

    return output


# In[ ]:

def expand(contacts,d,genome={}):
    """expand contacts by size d.  a genome (dict of chr:length) can be provided to stop a contact expanding past chromosomal boundaries."""
    
    header,contacts=_processFile(contacts)
    
    missing=set()
    if len(genome)!=0:
        for contact in contacts:
            contact[1]=max(0,contact[1]-d)
            contact[4]=max(0,contact[4]-d)
            if contact[0] in genome:
                contact[2]=min(genome[contact[0]],contact[2]+d)
            else:
                if contact[0] not in missing:
                    sys.stderr.write(contact[0]+" is not found in the genome file.")
                    missing.add(contact[0])
                contact[2]=contact[2]+d
            if contact[3] in genome:
                contact[5]=min(genome[contact[3]],contact[5]+d)
            else:
                if contact[3] not in missing:
                    sys.stderr.write(contact[3]+" is not found in the genome file.")
                    missing.add(contact[3])
                contact[5]=contact[5]+d
            
    else:
        for contact in contacts:
            contact[1]=max(0,contact[1]-d)
            contact[2]=contact[2]+d
            contact[4]=max(0,contact[4]-d)
            contact[5]=contact[5]+d
    delim="\t"
    contacts=[delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts]

    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output="\n".join(contacts)
    
    return output


# In[ ]:

def findLoops(contacts):
    """Find the internal regions (including anchors) to each entry in contacts."""
    _,contacts=_processFile(contacts)
    
    res=[]
    i=-1
    for contact in contacts:
        i+=1
        chromA=contact[0]
        startA=str(contact[1])
        stopA=str(contact[2])
        chromB=str(contact[3])
        startB=str(contact[4])
        stopB=str(contact[5])
        annots="\t".join(contact[6])
        if chromA==chromB:
            res.append("\t".join([chromA,startA,stopB,annots]))
        else:
            res.append("\t".join([chromA,startA,stopA,annots]))
            res.append("\t".join([chromB,startB,stopB,annots]))
        
    return ("\n".join(res))


# In[ ]:

def formatTripSparse(annotations,tripSparseMatrix):
    """Convert a Triplet Sparse Matrix file set to a PGL file."""
    annotationMap={line.split()[3]:"\t".join(line.split()[:3]) for line in annotations.split("\n")}

    output=""
    for line in tripSparseMatrix.split("\n"):
        line=line.split()
        output+=annotationMap[line[0]]+"\t"+annotationMap[line[1]]+"\t"+line[2]
    return output


# In[ ]:

def formatbedpe(FILENAME):
    """Convert a bedpe like file to a PGL file."""
    header=""
    lines=[]
    for line in FILENAME.split("\n"):
        if line[0]=="#":
            header+=line.strip()+"\n"
        else:
            lines.append(line.strip().split())
    contacts=[[x[0],int(x[1]),int(x[2]),x[3],int(x[4]),int(x[5]), x[6:]] for x in lines]
    header=header[:-2]
    i=0
    while i<len(contacts):
        contact=contacts[i]
        if contact[0] > contact[3]:
            contacts[i]=[contact[3],contact[4],contact[5],contact[0],contact[1],contact[2],contact[6]]
        elif contact[0]==contact[3]:
            if contact[1] > contact[4]:
                contacts[i]=[contact[3],contact[4],contact[5],contact[0],contact[1],contact[2],contact[6]]
            elif contact[1]==contact[4]:
                if contact[2] > contact[5]:
                    contacts[i]=[contact[3],contact[4],contact[5],contact[0],contact[1],contact[2],contact[6]]
        i+=1
    
    delim="\t"
    contacts=[delim.join([str(y) for y in x[:-1]])+delim+delim.join(x[-1]) for x in contacts]
    
    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(contacts)
    
    return output


# In[ ]:

def intersect(contactsA,contactsB,dashV=False,dashM=False,dashMC=False,dashU=False,useBAnnots=False,useAllAnnots=False,dashWO=False,dashWA=False,dashWB=False):
    """Find the intersecting PGLs of contactsA and contactsB"""
    
    header,contactsA=_processFile(contactsA)

    if _checkSorted(contactsA)==1:
        return ("contactsA is not sorted.  Please use PyGLtools.sort(contactsA)")

    elif _checkSorted(contactsA)==2:
        return ("contactsA is not a pgl file.  Please use PyGLtools.formatbedpe(contactsA)")
        
    _,contactsB=_processFile(contactsB)

    if _checkSorted(contactsB)==1:
        return ("contactsB is not sorted.  Please use PyGLtools.sort(contactsB)")
    elif _checkSorted(contactsB)==2:
        return ("contactsB is not a pgl file.  Please use PyGLtools.formatbedpe(contactsB)")
    
    #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    i=0
    k=0
    if dashM or dashMC or dashU:
        addedIs=set()
        addedKs=set()
    restartK=-1
    newPeaks=[]
    maximalRestart=0
    #compare file 2 to file 1, meaning advance file 2 first
    while i<len(contactsA) and k<len(contactsB):

        chrA1=contactsA[i][0]
        startA1=contactsA[i][1]
        endA1=contactsA[i][2]
        chrA2=contactsA[i][3]
        startA2=contactsA[i][4]
        endA2=contactsA[i][5]
        Aannotations=contactsA[i][6]
        
        if k==-1:
            k=0
        chrB1=contactsB[k][0]
        startB1=contactsB[k][1]
        endB1=contactsB[k][2]
        chrB2=contactsB[k][3]
        startB2=contactsB[k][4]
        endB2=contactsB[k][5]
        BAnnotations=contactsB[k][6]
        
        
        if endB1 > maximalRestart:
            maximalRestart=endB1
            
        #check chromosome on first bin
        if chrA1<chrB1:
            i+=1
            k=restartK
        elif chrA1>chrB1:
            k+=1
            restartK=k
            maximalRestart=0
            continue
        else:
            #on the same chromosome
            #we have a two options: first bins overlap or they dont.

            if startA1 < startB1 and endA1 < startB1:
                i+=1
                k=restartK
                continue
            elif startB1 < startA1 and endB1 < startA1:
                if maximalRestart<=startA1: #should always ==, < is present for my sanity
                    restartK=k
                k+=1
                continue

            else:
            #the bins overlap in some way.  Now we advance to bin2
                if chrA2!=chrB2:
                    k+=1
                    continue
                    

            #on the same chromosome
            #we have a two options: second bins overlap or they dont.

                if startA2 < startB2 and endA2 < startB2:
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1

                elif startB2 < startA2 and endB2 < startA2:
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1

            #bins overlap
                else:
                    if dashM or dashMC or dashU:
                        addedIs.add(i)
                        addedKs.add(k)
                    if dashV:
                        newPeaks.append(i)
                    elif dashM or dashMC:
                        chr1=chrA1
                        start1=min(startA1,startB1)
                        end1=max(endA1,endB1)
                        start2=min(startA2,startB2)
                        end2=max(endA2,endB2)
                        chr2=chrA2
                        if useBAnnots:
                            tempAnnots=["A,B"]
                            tempAnnots.extend(BAnnotations)
                            newPeaks.append([[chr1,start1,end1,chr2,start2,end2],tempAnnots])
                        elif useAllAnnots:
                            tempAnnots=["A,B"]
                            tempAnnots.extend(Aannotations)
                            tempAnnots.extend(BAnnotations)
                            newPeaks.append([[chr1,start1,end1,chr2,start2,end2],tempAnnots])
                        else:
                            tempAnnots=["A,B"]
                            tempAnnots.extend(Aannotations)
                            newPeaks.append([[chr1,start1,end1,chr2,start2,end2],tempAnnots])
                    elif dashWA:
                        if useBAnnots:
                            newPeaks.append([[chrA1,startA1,endA1,chrA2,startA2,endA2],BAnnotations])
                        elif useAllAnnots:
                            tempAnnots=Aannotations[:]
                            tempAnnots.extend(BAnnotations)
                            newPeaks.append([[chrA1,startA1,endA1,chrA2,startA2,endA2],tempAnnots])
                        else:
                            newPeaks.append([[chrA1,startA1,endA1,chrA2,startA2,endA2],Aannotations])
                    elif dashWB:
                        if useBAnnots:
                            newPeaks.append([[chrB1,startB1,endB1,chrB2,startB2,endB2],BAnnotations])
                        elif useAllAnnots:
                            tempAnnots=Aannotations[:]
                            tempAnnots.extend(BAnnotations)
                            newPeaks.append([[chrB1,startB1,endB1,chrB2,startB2,endB2],tempAnnots])
                        else:
                            newPeaks.append([[chrB1,startB1,endB1,chrB2,startB2,endB2],Aannotations])
                    elif dashWO:
                            overlapAnch1=str(max(endA1,endB1)-min(startA1,startB1)-abs(startA1-startB1)-abs(endA1-endB1))
                            overlapAnch2=str(max(endA2,endB2)-min(startA2,startB2)-abs(startA2-startB2)-abs(endA2-endB2))
                            tempAnnots=[chrB1,startB1,endB1,chrB2,startB2,endB2,overlapAnch1,overlapAnch2]
                            tempAnnots.extend(Aannotations)
                            tempAnnots.extend(BAnnotations)
                            newPeaks.append([[chrA1,startA1,endA1,chrA2,startA2,endA2],tempAnnots])
                    else:
                        chr1=str(chrA1)
                        start1=str(max(startA1,startB1))
                        end1=str(min(endA1,endB1))
                        start2=str(max(startA2,startB2))
                        end2=str(min(endA2,endB2))
                        chr2=str(chrA2)
                        if useBAnnots:
                            newPeaks.append([[chr1,start1,end1,chr2,start2,end2],BAnnotations])
                        elif useAllAnnots:
                            tempAnnots=Aannotations[:]
                            tempAnnots.extend(BAnnotations)
                            newPeaks.append([[chr1,start1,end1,chr2,start2,end2],tempAnnots])
                        else:
                            newPeaks.append([[chr1,start1,end1,chr2,start2,end2],Aannotations])
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1
                    
    if dashM:
        for i in range(len(contactsA)):
            if i not in addedIs:
                tempAnnots=["A"]
                tempAnnots.extend(contactsA[6])
                newPeaks.append([contactsA[i][:6],tempAnnots])
        for k in range(len(contactsB)):
            if k not in addedKs:
                tempAnnots=["B"]
                tempAnnots.extend(contactsB[6])
                newPeaks.append([contactsB[i][:6],tempAnnots])
    if dashV:
        newPeaks=[contactsA[i] for i in range(len(contactsA)) if i not in newPeaks]
    elif dashU:
        newPeaks=[contactsA[i] for i in range(len(contactsA)) if i in addedIs]
    
    delim="\t"
    
    if not dashV and not dashU:
        newPeaks=[delim.join([str(y) for y in x[0]])+delim+delim.join([str(y) for y in x[1]]) for x in newPeaks]
    else:
        newPeaks=[delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in newPeaks]

    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(newPeaks)
    
    return output


# In[ ]:

def intersect1D(contactsA,bedB,useBAnnots=False,useAllAnnots=False,aLocations=False,padA=0,padB=0,dashV=False):
    """Find the entries in bedB that intersect one or both anchors from contactsA"""
    
    #we will hash the bed file for instant lookup
    
    header,contactsA=_processFile(contactsA)

    if _checkSorted(contactsA)==1:
        return ("contactsA is not sorted.  Please use PyGLtools.sort(contactsA)")

    elif _checkSorted(contactsA)==2:
        return ("contactsA is not a pgl file.  Please use PyGLtools.formatbedpe(contactsA)")

    headerB,bedB=_processBedFile(bedB)

    
    if dashV:
        intersectedContactIndicies=set()
    newPeaks=[]
    #compare file 2 to file 1, meaning advance file 2 first
    for i in range(len(contactsA)): 
            chrA1=contactsA[i][0]
            startA1=max(contactsA[i][1]-padA,0)
            endA1=contactsA[i][2]+padA
            chrA2=contactsA[i][3]
            startA2=max(contactsA[i][4]-padA,0)
            endA2=contactsA[i][5]+padA
            difChrom=False
            
            if chrA1==chrA2:
                if chrA1 in bedB:
                    for k in range(len(bedB[chrA1])): 
                        Aannots=contactsA[i][6][:]

                        chrB=chrA1
                        startB=max(bedB[chrB][k][0]-padB,0)+1
                        endB=bedB[chrB][k][1]+padB
                        Bannots=bedB[chrB][k][2]

                        overlapA=False
                        overlapB=False
                        if startA1 < startB and endA1 < startB:
                            pass
                        elif startB < startA1 and endB < startA1:
                            pass
                        else:
                            overlapA=True

                        if startA2 < startB and endA2 < startB:
                            pass
                        elif startB < startA2 and endB < startA2:
                            pass
                        else:
                            overlapB=True

                        if overlapA and overlapB:
                            if dashV:
                                intersectedContactIndicies.add(i)
                                break
                            else:
                                if not aLocations:
                                    chr1=str(chrA1)
                                    start1=str(max(startA1,startB))
                                    end1=str(min(endA1,endB))
                                    start2=str(max(startA2,startB))
                                    end2=str(min(endA2,endB))
                                    chr2=str(chrA2)
                                else:
                                    chr1=chrA1
                                    start1=startA1
                                    end1=endA1
                                    chr2=chrA2
                                    start2=startA2
                                    end2=endA2
                                if useBAnnots:
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A,B"],Bannots])
                                elif useAllAnnots:
                                    for ann in Bannots:
                                        if ann not in Aannots:
                                            Aannots.append(ann)
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A,B"],Aannots])
                                else:
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A,B"],Aannots])

                        elif overlapA:
                            if dashV:
                                intersectedContactIndicies.add(i)
                                break
                            else:
                                if not aLocations:
                                    chr1=str(chrA1)
                                    start1=str(max(startA1,startB))
                                    end1=str(min(endA1,endB))
                                else:
                                    chr1=chrA1
                                    start1=startA1
                                    end1=endA1
                                chr2=chrA2
                                start2=startA2
                                end2=endA2
                                if useBAnnots:
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Bannots])
                                elif useAllAnnots:
                                    for ann in Bannots:
                                        if ann not in Aannots:
                                            Aannots.append(ann)
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Aannots])
                                else:
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Aannots])

                        elif overlapB:
                            if dashV:
                                intersectedContactIndicies.add(i)
                                break
                            else:
                                chr1=chrA1
                                start1=startA1
                                end1=endA1
                                if not aLocations:
                                    start2=str(max(startA2,startB))
                                    end2=str(min(endA2,endB))
                                    chr2=str(chrA2)
                                else:
                                    chr2=chrA2
                                    start2=startA2
                                    end2=endA2
                                if useBAnnots:
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Bannots])
                                elif useAllAnnots:
                                    for ann in Bannots:
                                        if ann not in Aannots:
                                            Aannots.append(ann)
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Aannots])
                                else:
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Aannots])

            else:
                if chrA1 in bedB:
                    for k in range(len(bedB[chrA1])):

                        chrB=chrA1
                        startB=max(bedB[chrB][k][0]-padB,0)+1
                        endB=bedB[chrB][k][1]+padB
                        Bannots=bedB[chrB][k][2]

                        difChrom=True
                        if startA1 < startB and endA1 < startB:
                            continue
                        elif startB < startA1 and endB < startA1:
                            break
                        else:
                            if dashV:
                                intersectedContactIndicies.add(i)
                                break
                            if not aLocations:
                                chr1=str(chrA1)
                                start1=str(max(startA1,startB))
                                end1=str(min(endA1,endB))
                            else:
                                chr1=chrA1
                                start1=startA1
                                end1=endA1
                            chr2=chrA2
                            start2=startA2
                            end2=endA2
                            if useBAnnots:
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Bannots])
                            elif useAllAnnots:
                                for ann in Bannots:
                                    if ann not in Aannots:
                                        Aannots.append(ann)
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Aannots])
                            else:
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Aannots])
                if chrA2 in bedB:    
                    for k in range(len(bedB[chrA2])):

                        chrB=chrA2
                        startB=max(bedB[chrB][k][0]-padB,0)+1
                        endB=bedB[chrB][k][1]+padB
                        Bannots=bedB[chrB][k][2]

                        if startA2 < startB and endA2 < startB:
                            continue
                        elif startB < startA2 and endB < startA2:
                            break
                        else:
                            if dashV:
                                intersectedContactIndicies.add(i)
                                break
                            chr1=chrA1
                            start1=startA1
                            end1=endA1
                            if not aLocations:
                                start2=str(max(startA2,startB))
                                end2=str(min(endA2,endB))
                                chr2=str(chrA2)
                            else:
                                chr2=chrA2
                                start2=startA2
                                end2=endA2
                            if useBAnnots:
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Bannots])
                            elif useAllAnnots:
                                for ann in Bannots:
                                    if ann not in Aannots:
                                        Aannots.append(ann)
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Aannots])
                            else:
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Aannots])
    if dashV:            
        newPeaks=[[contactsA[i][:5],contactsA[i][6]] for i in range(len(contactsA)) if i not in intersectedContactIndicies]
    
    delim="\t"            
    newPeaks=[delim.join([str(y) for y in x[0]])+delim+delim.join([str(y) for y in x[1]]) for x in newPeaks]
    
    
    if useBAnnots:
        if len(headerB)!=0:
            wholeHeaderB=headerB.split("\n")
            headerB=wholeHeaderB[-1].split("\t")
            part2=headerB[6:]
            headerB=headerB[:6]
            headerB.append("Intersected_Anchor")
            headerB.extend(part2)
            wholeHeaderB[-1]="\t".join(headerB)
            output="\n".join(wholeHeaderB)
    elif useAllAnnots:
        if len(headerB)!=0 or len(header)!=0:
            headerB=headerB.split("\n")
            header=header.split("\n")
            i=0
            output=""
            while i < len(headerB) or i < len(header):
                if i < len(header) and i < len(headerB):
                    output+=header[i]+"\n"+headerB[i]
                elif i < len(header):
                    output+=header[i]+"\n"
                else:
                    output+=headerB[i]+"\n"
                i+=1
    else:
        if len(header)!=0:
            output=header+"\n"
        else:
            output=""
    output+="\n".join(newPeaks)
    
    return output


# In[ ]:

def juicebox(contacts,nameCol=-1,colorCol=-1):
    """Format a PGL file for viewing in juicebox"""
    _,contacts=_processFile(contacts)

    minNumCols=min([6+len(y[-1]) for y in contacts])

    if any([x<1 and x!=-1 for x in [nameCol,colorCol]]):
        return "Valid column numbers must be given.  Column numbering starts with 1"
    if any([x>minNumCols for x in [nameCol,colorCol]]):
        return "A specified column exceeds the number of columns present in the file"

    
    
    res=[]
    i=-1
    for contact in contacts:
        i+=1
        chromA=contact[0]
        startA=str(contact[1])
        stopA=str(contact[2])
        chromB=str(contact[3])
        startB=str(contact[4])
        stopB=str(contact[5])
        if nameCol!=-1:
            name=contact[6][nameCol-6]
        else:
            name="Contact_"+str(i)
        if colorCol!=-1:
            color=contact[6][scoreCol-6]
        else:
            color="0,0,0"
        res.append("\t".join([chromA,startA,stopA,chromB,startB,stopB,name,color]))
            
    output="\t".join(["chr1","x1","x2","chr2","y1","y2","color","comment"])+"\n"
    output+="\n".join(res)
    
    return output


# In[ ]:

def merge(contacts,cols="%#$",commands="%#$",d=0,noHeader=False):
    """Merge entries from contacts that are distance d or closer on both anchors"""
    header,contacts=_processFile(contacts)

    if _checkSorted(contacts)==1:
        return ("contactsA is not sorted.  Please use PyGLtools.sort(contactsA)")

    elif _checkSorted(contacts)==2:
        return ("contactsA is not a pgl file.  Please use PyGLtools.formatbedpe(contactsA)")

    if cols!="%#$":
        cols=[int(x) for x in cols.split(',')]
        commands=commands.split(',')
    else:
        cols=[]
        commands=[]

    if len(cols)>0:
        if max(cols)>6+len(A[0][-1]):
            return ("A column argument surpassed the number of columns in the pgl file given")
    
    cols=[x-1 for x in cols]
    
    lastLen=-1
    while len(contacts)!=lastLen:
        lastLen=len(contacts)
        i=0
        endPoint=len(contacts)
        advanceI=False
        k=0
        newContacts=[]
        while i< endPoint:
            matchedNew=False
            if not advanceI:
                k+=1
            else:
                i+=1
                k=i+1
                advanceI=False
            if k >= endPoint:
                advanceI=True
                continue
            chrA1=contacts[i][0]
            startA1=contacts[i][1]
            endA1=contacts[i][2]
            chrA2=contacts[i][3]
            startA2=contacts[i][4]
            endA2=contacts[i][5]
            Aannotations=contacts[i][6]

            #check against all new contacts.  Then proceed
            j=0
            stop=len(newContacts)
            while j < stop:
                chrB1=newContacts[j][0]
                startB1=newContacts[j][1]
                endB1=newContacts[j][2]
                chrB2=newContacts[j][3]
                startB2=newContacts[j][4]
                endB2=newContacts[j][5]
                Bannotations=newContacts[j][6]
                if chrA1!=chrB1 or chrA2!=chrB2:
                    j+=1
                    continue
                else:
                    #on same chrom
                    if startA1 < startB1-d and endA1 < startB1-d:
                        j+=1
                        continue
                    elif startB1 < startA1-d and endB1 < startA1-d:
                        j+=1
                        continue
                    else:
                        #the first bins overlap
                        if startA2 < startB2-d and endA2 < startB2-d:
                            j+=1
                            continue
                        elif startB2 < startA2-d and endB2 < startA2-d:
                            j+=1
                            continue
                        else:
                            #the second bins overlap
                            if len(cols)>0:
                                newAnnotations=[]
                                for ind in range(len(cols)):
                                    if type(Aannotations[0])!=list:
                                        if commands[ind]=="count":
                                            newAnnotations.append([1])
                                        else:
                                            newAnnotations.append([Aannotations[cols[ind]-6]])
                                    else:
                                        newAnnotations.extend([Aannotations[ind]])
                                    newAnnotations[ind].extend(Bannotations[ind])                        
                            chr1=chrA1
                            start1=min(startA1,startB1)
                            end1=max(endA1,endB1)
                            start2=min(startA2,startB2)
                            end2=max(endA2,endB2)
                            chr2=chrA2
                            newContacts.append([chr1,start1,end1,chr2,start2,end2,newAnnotations])
                            newContacts.pop(j)
                            contacts.pop(i)
                            endPoint-=1
                            #this will basically keep i in the same place and reset k to i+1
                            i-=1
                            advanceI=True
                            matchedNew=True
                            break

            if matchedNew:
                continue

            chrB1=contacts[k][0]
            startB1=contacts[k][1]
            endB1=contacts[k][2]
            chrB2=contacts[k][3]
            startB2=contacts[k][4]
            endB2=contacts[k][5]
            Bannotations=contacts[k][6]

            if chrA1!=chrB1 or chrA2!=chrB2:
                advanceI=True
            else:
                #on same chrom
                if startA1 < startB1-d and endA1 < startB1-d:
                    advanceI=True
                elif startB1 < startA1-d and endB1 < startA1-d:
                    advanceI=True
                else:
                    #the first bins overlap
                    if startA2 < startB2-d and endA2 < startB2-d:
                        advanceI=False
                    elif startB2 < startA2-d and endB2 < startA2-d:
                        advanceI=False
                    else:
                        #the second bins overlap
                        newAnnotations=[]
                        if len(cols)>0:
                            if type(Aannotations[0])!=list:
                                for ind in range(len(cols)):
                                    newAnnotations.append([Aannotations[cols[ind]-6]])
                                    if type(Bannotations[0])!=list:
                                        newAnnotations[ind].append(Bannotations[cols[ind]-6])
                                    else:
                                        newAnnotations[ind].extend(Bannotations[ind]) 
                            else:
                                newAnnotations=Aannotations[:]
                                for ind in range(len(cols)):
                                    if type(Bannotations[0])!=list:
                                        newAnnotations[ind].append(Bannotations[cols[ind]-6])
                                    else:
                                        newAnnotations[ind].extend(Bannotations[ind])   
                        chr1=chrA1
                        start1=min(startA1,startB1)
                        end1=max(endA1,endB1)
                        start2=min(startA2,startB2)
                        end2=max(endA2,endB2)
                        chr2=chrA2
                        newContacts.append([chr1,start1,end1,chr2,start2,end2,newAnnotations])
                        contacts.pop(k)
                        contacts.pop(i)
                        endPoint-=2
                        #this will basically keep i in the same place and reset k to i+1
                        i-=1
                        advanceI=True


        contacts.extend(newContacts)
        contacts=[x if len(x[6])!=0 else [x[0],x[1],x[2],x[3],x[4],x[5],[x[6]]] for x in contacts]
    
    delim="\t"
    contacts=_processCommands(contacts,cols,commands,delim)
    
    if len(contacts[0])==6:
        contacts=[delim.join([str(y) for y in x]) for x in contacts]
    else:
        contacts=[delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts]
        
    useOld=False
    if len(header)>0:
        if len(header[0].split())>6+len(contacts[0][-1]):
            useOld=True
    if not noHeader:
        output=_createHeader(header.split(),cols,commands,useOld)
    else:
        output=""
    output+="\n".join(contacts)
    
    return output


# In[ ]:

def samTopgl(samfile,delim="\t",insertSize=1000):
    """Convert a sam file to a PGL file for use with PyGLtools.coverage"""
    
    
    
    #reads are stored as name,chrom,start,end
    reads=[]
    contacts=[]
    header=""
    for line in samfile.split("\n"):
        if line[0]=="#":
            header+=line+"\n"
            continue
        line=line.split()
        if len(reads)==0:
            if line[1]=="16":
                reads.append(_processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],True))
            else:
                reads.append(_processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],False))
        elif reads[-1][0].split(delim)[0]==line[0].split(delim)[0]:
            if line[1]=="16":
                reads.append(_processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],True))
            else:
                reads.append(_processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],False))
        else:
            if len(reads)<2:
                pass
            elif len(reads)==2:
                if reads[0][1]<reads[1][1]:
                    contacts.append([reads[0][1],reads[0][2],reads[0][3],reads[1][1],reads[1][2],reads[1][3],reads[0][0]+","+reads[1][0]])
                elif reads[0][1]>reads[1][1]:
                    contacts.append([reads[1][1],reads[1][2],reads[1][3],reads[0][1],reads[0][2],reads[0][3],reads[1][0]+","+reads[0][0]])
                else:
                    if reads[0][2]<reads[1][2]:
                        contacts.append([reads[0][1],reads[0][2],reads[0][3],reads[1][1],reads[1][2],reads[1][3],reads[0][0]+","+reads[1][0]])
                    elif reads[0][2]>reads[1][2]:
                        contacts.append([reads[1][1],reads[1][2],reads[1][3],reads[0][1],reads[0][2],reads[0][3],reads[1][0]+","+reads[0][0]])
            else:
                
                groupedReads={}
                for read in reads:
                    if read[1] in groupedReads:
                        groupedReads[read[1]].append(read)
                    else:
                        groupedReads[read[1]]=[read]
                if len(groupedReads.keys()) > 2:
                    pass
                elif len(groupedReads.keys()) == 1:
                    group1=[]
                    group2=[]
                    reads=sorted(reads,key=lambda x: x[2])
                    onGroup2=False
                    for read in reads:
                        if len(group1) > 0:
                            if abs(group1[-1][2]-read[2])>insertSize:
                                    onGroup2=True
                        if onGroup2:
                            group2.append(read)
                        else:
                            group1.append(read)
                    
                    if len(group2) > 0:
                        chrA=group1[0][1]
                        startA=min(x[2] for x in group1)
                        endA=max(x[3] for x in group1)

                        chrB=group2[0][1]
                        startB=min(x[2] for x in group2)
                        endB=max(x[3] for x in group2)
                        name=",".join([read[0] for read in reads])     

                        contacts.append([chrA,startA,endA,chrB,startB,endB,name])
                else:
                    outsideInsertSize=False
                    for group in groupedReads:
                        for i in range(len(groupedReads[group])):
                            for j in range(i+1,len(groupedReads[group])):
                                if abs(groupedReads[group][j][2]-groupedReads[group][i][2])>insertSize:
                                     outsideInsertSize=True
                    if outsideInsertSize:
                        pass
                    else:
                        chroms=sorted(groupedReads.keys())
                        
                        chrA=groupedReads[chroms[0]][0][1]
                        startA=min(x[2] for x in groupedReads[chrA])
                        endA=max(x[3] for x in groupedReads[chrA])
                        chrB=groupedReads[chroms[0]][0][1]
                        startB=min(x[2] for x in groupedReads[chrB])
                        endB=max(x[3] for x in groupedReads[chrB])
                        name=",".join([",".join([x[0] for x in groupedReads[group]]) for group in groupedReads])     
                        
                        contacts.append([chrA,startA,endA,chrB,startB,endB,name])
            reads=[[line[0],line[2],int(line[3]),int(line[3])-len(line[9])]]
            
    if len(reads)<2:
        pass
    elif len(reads)==2:
        if reads[0][1]<reads[1][1]:
            contacts.append([reads[0][1],reads[0][2],reads[0][3],reads[1][1],reads[1][2],reads[1][3],reads[0][0]+","+reads[1][0]])
        elif reads[0][1]>reads[1][1]:
            contacts.append([reads[1][1],reads[1][2],reads[1][3],reads[0][1],reads[0][2],reads[0][3],reads[1][0]+","+reads[0][0]])
        else:
            if reads[0][2]<reads[1][2]:
                contacts.append([reads[0][1],reads[0][2],reads[0][3],reads[1][1],reads[1][2],reads[1][3],reads[0][0]+","+reads[1][0]])
            elif reads[0][2]>reads[1][2]:
                contacts.append([reads[1][1],reads[1][2],reads[1][3],reads[0][1],reads[0][2],reads[0][3],reads[1][0]+","+reads[0][0]])
    else:           
        groupedReads={read[0]:read for read in reads}             
        if len(groupedReads.keys()) > 2:
            pass
        elif len(groupedReads.keys()) == 1:
                    group1=[]
                    group2=[]
                    reads=sorted(reads,key=lambda x: x[2])
                    onGroup2=False
                    for read in reads:
                        if len(group1) > 0:
                            if abs(group1[-1][2]-read[2])>insertSize:
                                    onGroup2=True
                        if onGroup2:
                            group2.append(read)
                        else:
                            group1.append(read)
                    
                    if len(group2) > 0:
                        chrA=group1[0][1]
                        startA=min(x[2] for x in group1)
                        endA=max(x[3] for x in group1)

                        chrB=group2[0][1]
                        startB=min(x[2] for x in group2)
                        endB=max(x[3] for x in group2)
                        name=",".join([read[0] for read in reads])     

                        contacts.append([chrA,startA,endA,chrB,startB,endB,name])
        else:
            outsideInsertSize=False
            for group in groupedReads:
                for i in range(len(groupedReads[group])):
                    for j in range(i+1,len(groupedReads[group])):
                        if abs(groupedReads[group][j][2]-groupedReads[group][i][2])>insertSize:
                             outsideInsertSize=True
            if outsideInsertSize:
                pass
            else:
                chroms=sorted(groupedReads.keys())

                chrA=groupedReads[chroms[0]][1]
                startA=min(x[2] for x in groupedReads[chrA])
                endA=max(x[3] for x in groupedReads[chrA])
                chrB=groupedReads[chroms[0]][1]
                startA=min(x[2] for x in groupedReads[chrB])
                startB=max(x[3] for x in groupedReads[chrB])
                name=",".join([",".join([x[0] for x in groupedReads[group]]) for group in groupedReads])     
                contacts.append([chrA,startA,stopA,chrB,startB,endB,name])
    
    contacts=["\t".join([str(y) for y in x]) for x in contacts]

    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(contacts)
    
    return output


# In[ ]:

def subtract(contactsA,contactsB):
    """Find the non overlapping parts of PGLs from contactsA and contactsB"""
    
    header,contactsA=_processFile(contactsA)

    if _checkSorted(contactsA)==1:
        return ("contactsA is not sorted.  Please use PyGLtools.sort(contactsA)")

    elif _checkSorted(contactsA)==2:
        return ("contactsA is not a pgl file.  Please use PyGLtools.formatbedpe(contactsA)")
        
    _,contactsB=_processFile(contactsB)

    if _checkSorted(contactsB)==1:
        return ("contactsB is not sorted.  Please use PyGLtools.sort(contactsB)")
    elif _checkSorted(contactsB)==2:
        return ("contactsB is not a pgl file.  Please use PyGLtools.formatbedpe(contactsB)")
    
    #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    i=0
    k=0
    restartK=-1
    newPeaks=[]
    maximalRestart=0
    #compare file 2 to file 1, meaning advance file 2 first
    while i<len(contactsA) and k<len(contactsB):
            
        chrA1=contactsA[i][0]
        startA1=contactsA[i][1]
        endA1=contactsA[i][2]
        chrA2=contactsA[i][3]
        startA2=contactsA[i][4]
        endA2=contactsA[i][5]
        Aannotations=contactsA[i][6]

        if k==-1:
            k=0
        chrB1=contactsB[k][0]
        startB1=contactsB[k][1]
        endB1=contactsB[k][2]
        chrB2=contactsB[k][3]
        startB2=contactsB[k][4]
        endB2=contactsB[k][5]

        if endB1 > maximalRestart:
            maximalRestart=endB1
        
        #check chromosome on first bin
        if chrA1<chrB1:
            i+=1
            k=restartK
        elif chrA1>chrB1:
            k+=1
            restartK=k
            maximalRestart=0
            continue
        else:
            #on the same chromosome
            #we have a two options: first bins overlap or they dont.

            if startA1 < startB1 and endA1 < startB1:
                i+=1
                k=restartK
                continue
            elif startB1 < startA1 and endB1 < startA1:
                if maximalRestart<=startA1: #should always ==, < is present for my sanity
                    restartK=k
                k+=1
                continue

            else:
            #the bins overlap in some way.  Now we advance to bin2
                if restartK==-1:
                    restartK=k
                if chrA2!=chrB2:
                    k+=1
                    continue
                    

            #on the same chromosome
            #we have a two options: second bins overlap or they dont.

                if startA2 < startB2 and endA2 < startB2:
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1

                elif startB2 < startA2 and endB2 < startA2:
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1


                else:
                    #both bins overlap in some fashion.
                    chrC1=chrA1
                    chrC2=chrA2
                    if startB1<=startA1  and endA1<=endB1:
                        pass
                    elif startB2<=startA2  and endA2<=endB2:
                        pass
                    else:
                        if startA1 < startB1 and endA1 > endB1:
                            if startA2 < startB2 and endA2 > endB2:
                                
                                newPeaks.extend([[chrA1,startA1,startB1,chrA2,startA2,startB2,Aannotations],
                                                 [chrA1,startA1,startB1,chrA2,endA2,endB2,Aannotations],
                                                 [chrA1,endA1,endB1,chrA2,startA2,startB2,Aannotations],
                                                 [chrA1,endA1,endB1,chrA2,endA2,endB2,Aannotations]])
                            
                            else:
                                
                                if startB2 < startA2:
                                
                                    newPeaks.extend([[chrA1,startA1,startB1,chrA2,endB2,endA2,Aannotations],
                                                     [chrA1,endB1,endA1,chrA2,endB2,endA2,Aannotations]])
                                else:
                                    
                                    newPeaks.extend([[chrA1,startA1,startB1,chrA2,startA2,startB2,Aannotations],
                                                     [chrA1,endB1,endA1,chrA2,startA2,startB2,Aannotations]])
                                    
                                
                        elif startA2 < startB2 and endA2 > endB2:
                            
                                if startA1 < startB1:
                                
                                    newPeaks.extend([[chrA1,startA1,startB1,chrA2,startA2,startB2,Aannotations],
                                                     [chrA1,startA1,startB1,chrA2,endB2,endA2,Aannotations]])
                                else:
                                    
                                    newPeaks.extend([[chrA1,endB1,endA1,chrA2,startA2,startB2,Aannotations],
                                                     [chrA1,endB1,endA1,chrA2,endB2,endA2,Aannotations]])
                                
                        else:
                            
                                if startA1 < startB1:
                                    
                                    if startA2 < startB2:
                                        
                                        newPeaks.extend([[chrA1,startA1,startB1,chrA2,startA2,startB2,Aannotations]])
                                        
                                    else:
                                        
                                        newPeaks.extend([[chrA1,startA1,startB1,chrA2,endB2,endA2,Aannotations]])
                                
                                elif startA2 < startB2:
                                    
                                        newPeaks.extend([[chrA1,endB1,endA1,chrA2,startA2,startB2,Aannotations]])
                                        
                                else:
                                    
                                        newPeaks.extend([[chrA1,endB1,endA1,chrA2,endB2,endA2,Aannotations]])
                                       
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1
    
    
    delim="\t"
    
    newPeaks=[delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in newPeaks]

    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(newPeaks)
    
    return output


# In[ ]:

def subtract1D(contactsA,bedB):
    """Find the parts of PGLs from contactsA that do not overlap entries in bedB"""
    
    header,contactsA=_processFile(contactsA)

    if _checkSorted(contactsA)==1:
        return ("contactsA is not sorted.  Please use PyGLtools.sort(contactsA)")

    elif _checkSorted(contactsA)==2:
        return ("contactsA is not a pgl file.  Please use PyGLtools.formatbedpe(contactsA)")

    headerB,bedB=_processBedFile(bedB)

        
    #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    newPeaks=[]
    #compare file 2 to file 1, meaning advance file 2 first
    for i in range(len(contactsA)):
        chrA1=contactsA[i][0]
        startA1=contactsA[i][1]
        endA1=contactsA[i][2]
        chrA2=contactsA[i][3]
        startA2=contactsA[i][4]
        endA2=contactsA[i][5]
        Aannots=contactsA[i][6]

        if chrA1==chrA2:
            if chrA1 in bedB:
                for k in range(len(bedB[chrA1])):
                    chrB=chrA1
                    startB=bedB[chrB][k][0]+1
                    endB=bedB[chrB][k][1]

                    if startA1 < startB and endA1 < startB:
                        pass
                    elif startB < startA1 and endB < startA1:
                        pass
                    else:
                        newPeaks.extend(_processSubtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,1))

                    if startA2 < startB and endA2 < startB:
                        pass
                    elif startB < startA2 and endB < startA2:
                        pass
                    else:
                        newPeaks.extend(_processSubtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,2))


        else:
            if chrA1 in bedB:
                for k in range(len(bedB[chrA1])):
                    chrB=chrA1
                    startB=bedB[chrB][k][0]+1
                    endB=bedB[chrB][k][1]

                    if startA1 < startB and endA1 < startB:
                        continue
                    elif startB < startA1 and endB < startA1:
                        break
                    else:
                        newPeaks.extend(_processSubtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,1))

            if chrA2 in bedB:
                for k in range(len(bedB[chrA2])):
                    chrB=chrA2
                    startB=bedB[chrB][k][0]+1
                    endB=bedB[chrB][k][1]

                    if startA2 < startB and endA2 < startB:
                        continue
                    elif startB < startA2 and endB < startA2:
                        break
                    else:
                        newPeaks.extend(_processSubtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,2))
    
    delim="\t"
    
    newPeaks=[delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in newPeaks if len(x)!=0]
    
    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(newPeaks)
    
    return output


# In[ ]:

def window(contacts,window1="%#$",window2="%#$"):
    """filter contacts on window1 for anchors A and window2 for anchorsB"""
    
    header,contacts=_processFile(contacts)

    if "-" in window1 and ":" in window1:
        window1=[window1.split(":")[0],int(window1.split(":")[1].split("-")[0]),int(window1.split(":")[1].split("-")[1])]
    elif window1!="%#$":
        window1=[window1]
    else:
        window1=[]
    if "-" in window2 and ":" in window2:
        window2=[window2.split(":")[0],int(window2.split(":")[1].split("-")[0]),int(window2.split(":")[1].split("-")[1])]
    elif window2!="%#$":
        window2=[window2]
    else:
        window2=[]

    # filter contactsA on window1 and contactsB on window2.  If one is not supplied, only filter on the one that is present
    if len(window1)==3 and len(window2)==3:
        contacts=[x for x in contacts if window1[0]==x[0] and window1[1]<=x[1] and window1[2]>=x[2] and window2[0]==x[3] and window2[1]<=x[4] and window2[2]>=x[5]]
    elif len(window1)==3 and len(window2)==0:
        contacts=[x for x in contacts if window1[0]==x[0] and window1[1]<=x[1] and window1[2]>=x[2]]
    elif len(window2)==3 and len(window1)==0:
        contacts=[x for x in contacts if window2[0]==x[3] and window2[1]<=x[4] and window2[2]>=x[5]]
    elif len(window1)==3 and len(window2)==1:
        contacts=[x for x in contacts if window1[0]==x[0] and window1[1]<=x[1] and window1[2]>=x[2] and window2[0]==x[3]]
    elif len(window2)==3 and len(window1)==1:
        contacts=[x for x in contacts if window2[0]==x[3] and window2[1]<=x[4] and window2[2]>=x[5] and window1[0]==x[0]]   
    elif len(window1)==1 and len(window2)==1:
        contacts=[x for x in contacts if window1[0]==x[0] and window2[0]==x[3]]
    elif len(window1)==1:
        
        contacts=[x for x in contacts if window1[0]==x[0]]
    elif len(window2)==1:
        contacts=[x for x in contacts if window2[0]==x[3]]
    
    
    delim="\t"
    
    contacts=[delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts]

    if len(header)!=0:
        output=header+"\n"
    else:
        output=""
    output+="\n".join(contacts)
    
    return output


