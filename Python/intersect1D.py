
# coding: utf-8

# In[1]:

import argparse
import sys
from pgltools_library import *


# In[ ]:

parser=argparse.ArgumentParser()
parser._optionals.title = "Arguments"
parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
parser.add_argument('-stdInA',help="Will use stdin for file a.  ", required=False,action='store_true')
parser.add_argument('-b',help="File Path for file b.  Required for merge and intersect unless -stdInB is used", required=False,default="%#$")
parser.add_argument('-stdInB',help="Will use stdin for file b.",action='store_true')
parser.add_argument('-bA',help="Keep the annotations from the bed file instead of the be2d file.",action='store_true')
parser.add_argument('-allA',help="Keep the annotations from the bed file as well as the be2d file.",action='store_true')
parser.add_argument('-aL',help="Output original contacts rather than intersection when a region is found.",action='store_true')
parser.add_argument('-pA',help="Add specified padding for contacts.",required=False,default=0,type=int)
parser.add_argument('-pB',help="Add specified padding for bed.",required=False,default=0,type=int)
args = vars(parser.parse_args())


# In[ ]:

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)


# In[ ]:

if args['stdInB'] and args['stdInA']:
    print "stdin can only be used for either a or b"
    exit(1)
if args['stdInA']==False and args['a']=="%#$":
    print "either -stdInA or -a must be used"
    exit(1)
if args['stdInB']==False and args['b']=="%#$":
    print "either -stdInB or -b must be used"
    exit(1)
if args['bA']==True and args['allA']==True:
    print "-bA and -allA cannot be used at the same time"
    exit(1)


# In[ ]:

def formatContacts(contacts,delim):
    return [delim.join([str(y) for y in x[0]])+delim+delim.join([str(y) for y in x[1]]) for x in contacts]


# In[27]:

def overlap1D(contactsA,bedB,useBAnnots,useAllAnnots,aLocations,padA,padB):
    #we will hash the bed file for instant lookup
    
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
                for k in range(len(bedB[chrA1])): 
                    Aannots=contactsA[i][6][:]

                    chrB=chrA1
                    startB=max(bedB[chrB][k][0]-padB,0)
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
                for k in range(len(bedB[chrA1])):
                    
                    chrB=chrA1
                    startB=max(bedB[chrB][k][0]-padB,0)
                    endB=bedB[chrB][k][1]+padB
                    Bannots=bedB[chrB][k][2]
                    
                    difChrom=True
                    if startA1 < startB and endA1 < startB:
                        continue
                    elif startB < startA1 and endB < startA1:
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
                    
                for k in range(len(bedB[chrA2])):
                    
                    chrB=chrA2
                    startB=max(bedB[chrB][k][0]-padB,0)
                    endB=bedB[chrB][k][1]+padB
                    Bannots=bedB[chrB][k][2]
                    
                    if startA2 < startB and endA2 < startB:
                        continue
                    elif startB < startA2 and endB < startA2:
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
                
    return newPeaks


# In[ ]:

if args['stdInA']:
    header,A=processStdin()
else:
    header,A=processFile(args['a'])
    
if checkSorted(A)==1:
    print ("File A is not sorted.  Please use pgltools sort [FILE]")
    exit()
elif checkSorted(A)==2:
    print ("File A is not a pgl file.  Please use pgltools formatpgl [FILE]")
    exit()


if args["b"]!="%#$":
    headerB,B=processBedFile(args['b'])
if args['stdInB']:
    headerB,B=processStdinBed()

res=overlap1D(A,B,args['bA'],args['allA'],args['aL'],args['pA'],args['pB'])
res=formatContacts(res,"\t")

if args['bA']:
    if len(headerB)!=0:
        wholeHeaderB=headerB.split("\n")
        headerB=wholeHeaderB[-1].split("\t")
        part2=headerB[6:]
        headerB=headerB[:6]
        headerB.append("Intersected_Anchor")
        headerB.extend(part2)
        wholeHeaderB[-1]="\t".join(headerB)
        print ("\n".join(wholeHeaderB))
elif args['allA']:
    if len(headerB)!=0 or len(header)!=0:
        headerB=headerB.split("\n")
        header=header.split("\n")
        i=0
        while i < len(headerB) or i < len(header):
            if i < len(header) and i < len(headerB):
                print(header[i]+"\n"+headerB[i])
            elif i < len(header):
                print(header[i]+"\n")
            else:
                print(headerB[i]+"\n")
            i+=1
else:
    if len(header)!=0:
        print(header)
print("\n".join(res))


