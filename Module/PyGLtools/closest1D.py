
# coding: utf-8

# In[ ]:

import argparse
import sys
from pgltools_library import *


# In[ ]:

def _formatClosest1D(contacts,delim):
    return [delim.join([delim.join([str(y) for y in x[0]]),delim.join([str(y) for y in x[1]])]) for x in contacts]


# In[ ]:

def _closest1D(contactsA,bedB,dashBA):
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
                    startB=bedB[chrA1][k][0]
                    endB=bedB[chrA1][k][1]
                    if startB!=endB:
                        startB+=1
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
                    startB=bedB[chrA1][k][0]
                    endB=bedB[chrA1][k][1]
                    if startB!=endB:
                        startB+=1
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
                        startB=bedB[chrA1][k][0]
                        endB=bedB[chrA1][k][1]
                        if startB!=endB:
                            startB+=1
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
                
    return newPeaks


# In[ ]:

def closest1D(A,B,args):
    res=_closest1D(A,B,args['ba'])

    res=_formatClosest1D(res,"\t") 

    if __name__=="__main__":
        if len(res)!=0:
            try:
                if not args['ba']:
                    print "\t".join(["#chrA","startA","stopA","chrB","startB","stopB","closestChr","closestStart","closestStop","distance"])
                else:
                    print "\t".join(["#chrA","startA","stopA","chrB","startB","stopB","closestAChr","closestAStart","closestAStop",
                                     "distanceToA","closestBChr","closestBStart","closestBStop","distanceToB"])

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

if __name__=="__main__":
    #parse arguments
    parser=argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False)
    parser.add_argument('-stdInA',help="Will use stdin for file a.  ", required=False,action='store_true')
    parser.add_argument('-b',help="File Path for file b.  Required unless -stdInB is used", required=False,default="%#$")
    parser.add_argument('-stdInB',help="Will use stdin for file b.",action='store_true')
    parser.add_argument('-ba',help="Report the closest feature for each anchor in the PGL, rather than the absolute closest feature.",action='store_true')
    args = vars(parser.parse_args())

    #show help if no arguments passed
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #validate arguments
    if args['stdInB'] and args['stdInA']:
        print "stdin can only be used for either a or b"
        exit(1)
    elif args['stdInA']==False and args['a']=="%#$":
        print "either -stdInA or -a must be used"
        exit(1)
    elif args['stdInB']==False and args['b']=="%#$":
        print "either -stdInB or -b must be used"
        exit(1)



    if args['stdInA']:
        header,A=processStdin()
    else:
        header,A=processFile(args['a'])

    if args["b"]!="%#$":
        _,B=processBedFile(args['b'])
    if args['stdInB']:
        _,B=processStdinBed()

    closest1D(A,B,args)


