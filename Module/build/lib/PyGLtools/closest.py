
# coding: utf-8

# In[5]:


import argparse
import sys
from pgltools_library import *


# In[16]:


def _formatClosest2DOutput(contacts,delim):
    return [delim.join([delim.join([str(y) for y in x[0]]),delim.join([str(y) for y in x[1]]),str(x[2]),delim.join(x[3])]) for x in contacts]


# In[1]:


def _closest2D(contactsA,contactsB,reportAAnnots,reportBAnnots):
     #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    newPeaks=[]
    #compare file 2 to file 1, meaning advance file 2 first
    for k in range(len(contactsB)):
        distance=-1
        closestFeature=[]
        for i in range(len(contactsA)):
            
            chrA1=contactsA[i][0]
            startA1=contactsA[i][1]
            endA1=contactsA[i][2]
            chrA2=contactsA[i][3]
            startA2=contactsA[i][4]
            endA2=contactsA[i][5]
            annotA=contactsA[i][6]

            chrB1=contactsB[k][0]
            startB1=contactsB[k][1]
            endB1=contactsB[k][2]
            chrB2=contactsB[k][3]
            startB2=contactsB[k][4]
            endB2=contactsB[k][5]
            annotB=contactsB[k][6]

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
                    closestFeature=[i]
                elif bin1Dist+bin2Dist == distance:
                    closestFeature.append(i)

                    
        if reportAAnnots:
            if reportBAnnots:
                annots=annotA[:]
                annots.extend(annotB)
            else:
                annots=annotA[:]
        else:
            if reportBAnnots:
                annots=annotB[:]
            else:
                annots=[]
        if len(closestFeature)>0:
            for cf in closestFeature:
                newPeaks.append([contactsB[k][:6],contactsA[cf][:6],distance,annots])
        else:
            newPeaks.append([contactsB[k][:6],[".",".",".",".",".","."],".",annots])
                
    return newPeaks


# In[10]:


def closest2D(A,B,headerA,headerB,aA,bA):
    res=_closest2D(B,A,bA,aA) #keep flipping consistent
    res=_formatClosest2DOutput(res,"\t")
    #print a new header
    if __name__=="__main__":
        if len(res)!=0:
            try:
                newHeader=["#fileA_chrA","fileA_startA","fileA_stopA","fileA_chrB","fileA_startB","fileA_stopB",
                                 "fileB_chrA","fileB_startA","fileB_stopA","fileB_chrB","fileB_startB","fileB_stopB","Distance"]
                if aA:
                    newHeader.extend(headerA.split()[6:])
                if bA:
                    newHeader.extend(headerB.split()[6:])
                print "\t".join(newHeader)
                print("\n".join(res))
            except IOError as e:
                if e.errno==32:
                    exit()
    else:
        funcOut=[]
        for r in res:
            r=r.split("\t")
            funcOut.append([r[0],int(r[1]),int(r[2]),r[3],int(r[4]),int(r[5]),r[6:]])
        return funcOut


# In[ ]:


if __name__ == "__main__":
    # parse arguments
    parser=argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
    parser.add_argument('-stdInA',help="Will use stdin for file a.  ", required=False,action='store_true')
    parser.add_argument('-b',help="File Path for file b.  Required for merge and intersect unless -stdInB is used", required=False,default="%#$")
    parser.add_argument('-stdInB',help="Will use stdin for file b.",action='store_true')
    parser.add_argument('-aA',help="Report annotations for anchor A.",action='store_true')
    parser.add_argument('-bA',help="Report annotations for anchor B.  If used with aA, A annots will come first.",action='store_true')
    args = vars(parser.parse_args())

    # print help with no arguments passed
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #check validity of arguments used
    if args['stdInB'] and args['stdInA']:
        print "stdin can only be used for either a or b"
        exit(1)
    elif args['stdInA']==False and args['a']=="%#$":
        print "either -stdInA or -a must be used"
        exit(1)
    elif args['stdInB']==False and args['b']=="%#$":
        print "either -stdInB or -b must be used"
        exit(1)
        
    #process the input files

    if args['stdInA']:
        headerA,A=processStdin()
    else:
        headerA,A=processFile(args['a'])

    if args["b"]!="%#$":
        headerB,B=processFile(args['b'])
    if args['stdInB']:
        headerB,B=processStdin()


    closest2D(A,B,headerA,headerB,args['aA'],args['bA'])


