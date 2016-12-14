
# coding: utf-8

# In[ ]:

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

def closest2D(contactsA,contactsB):
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
            newPeaks.append([contactsB[k][:6],contactsA[closestFeature][:6]])
        else:
            newPeaks.append([contactsB[k][:6],[".",".",".",".",".","."]])
                
    return newPeaks


# In[ ]:

if args['stdInA']:
    header,A=processStdin()
else:
    header,A=processFile(args['a'])

if args["b"]!="%#$":
    _,B=processFile(args['b'])
if args['stdInB']:
    _,B=processStdin()
    

res=closest2D(B,A)
res=formatDoubleContacts(res,"\t")
if len(header)!=0:
    print(header)
print("\n".join(res))


