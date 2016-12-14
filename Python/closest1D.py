
# coding: utf-8

# In[ ]:

import argparse
import sys
from pgltools_library import *


# In[ ]:

parser=argparse.ArgumentParser()
parser._optionals.title = "Arguments"
parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False)
parser.add_argument('-stdInA',help="Will use stdin for file a.  ", required=False,action='store_true')
parser.add_argument('-b',help="File Path for file b.  Required unless -stdInB is used", required=False,default="%#$")
parser.add_argument('-stdInB',help="Will use stdin for file b.",action='store_true')
args = vars(parser.parse_args())


# In[ ]:

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)


# In[ ]:

if args['stdInB'] and args['stdInA']:
    print "stdin can only be used for either a or b"
    exit(1)
elif args['stdInA']==False and args['a']=="%#$":
    print "either -stdInA or -a must be used"
    exit(1)
elif args['stdInB']==False and args['b']=="%#$":
    print "either -stdInB or -b must be used"
    exit(1)


# In[ ]:

def formatDoubleContacts(contacts,delim):
    return [delim.join([delim.join([str(y) for y in x[0]]),delim.join([str(y) for y in x[1]])]) for x in contacts]


# In[ ]:

def closest1D(contactsA,bedB):
     #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    newPeaks=[]
    #compare file 2 to file 1, meaning advance file 2 first
    for i in range(len(contactsA)):
        distance=-1
        closestFeature=-1

        chrA1=contactsA[i][0]
        startA1=contactsA[i][1]
        endA1=contactsA[i][2]
        chrA2=contactsA[i][3]
        startA2=contactsA[i][4]
        endA2=contactsA[i][5]

        if chrA1==chrA2:
            for k in range(len(bedB[chrA1])):
                chrB=chrA1
                startB=bedB[chrA1][k][0]
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

                if minDist < distance or distance==-1:
                    distance=minDist
                    closestFeature=(chrB,k)

        else:
            for k in range(len(bedB[chrA1])):
                chrB=chrA1
                startB=bedB[chrA1][k][0]
                endB=bedB[chrA1][k][1]
                if startA1 < startB and endA1 < startB:
                    bin1Dist=startB-endA1
                elif startB < startA1 and endB < startA1:
                    bin1Dist=startA1-endB
                else:
                    bin1Dist=0
                if bin1Dist < distance or distance==-1:
                    distance=minDist
                    closestFeature=(chrB,k)

        for k in range(len(bedB[chrA2])):
                chrB=chrA2
                startB=bedB[chrA1][k][0]
                endB=bedB[chrA1][k][1]
                if startA2 < startB and endA2 < startB:
                    bin2Dist=startB-endA2
                elif startB < startA2 and endB < startA2:
                    bin2Dist=startA2-endB
                else:
                    bin2Dist=0
                if bin2Dist < distance or distance==-1:
                    distance=minDist
                    closestFeature=(chrB,k)

        if closestFeature!=-1:
            entry=[closestFeature[0]]
            entry.extend(bedB[closestFeature[0]][closestFeature[1]][:2])
            newPeaks.append([contactsA[i][:6],entry])
        else:
            newPeaks.append([contactsA[i][:6],[".",".","."]])
                
    return newPeaks


# In[ ]:

if args['stdInA']:
    header,A=processStdin()
else:
    header,A=processFile(args['a'])
    
if args["b"]!="%#$":
    _,B=processBedFile(args['b'])
if args['stdInB']:
    _,B=processStdinBed()

res=closest1D(A,B)
    
res=formatDoubleContacts(res,"\t") 

if len(header)!=0:
    print(header)
print("\n".join(res))


