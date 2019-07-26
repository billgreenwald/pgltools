
# coding: utf-8

# In[17]:


import argparse
import sys
from pgltools_library import *


# In[7]:


def _formatContacts(contacts,delim):
    return [delim.join([str(y) for y in x[0]])+delim+delim.join([str(y) for y in x[1]]) for x in contacts]


# In[8]:


def _formatContactsV(contacts,delim):
    return [delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts]


# In[15]:


def _overlap2D(contactsA,contactsB,dashV,dashM,dashMC,dashU,useBAnnots,useAllAnnots,dashWO,dashWA,dashWB,dist):
    #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    i=0
    k=0
    maximalRestart=0
    if dashM or dashMC or dashU:
        addedIs=set()
        addedKs=set()
    restartK=-1
    newPeaks=[]
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
            restartK=k
            maximalRestart=0
            k+=1
            continue
        else:
            #on the same chromosome
            #we have a two options: first bins overlap or they dont.

            if startA1 < startB1-dist and endA1 <= startB1-dist:
                i+=1
                k=restartK
                continue
            elif startB1 < startA1-dist and endB1<= startA1-dist:
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

                if startA2 < startB2-dist and endA2 <= startB2-dist:
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1

                elif startB2 < startA2-dist and endB2 <= startA2-dist:
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
        AannotLen=len(contactsA[0][6])
        BannotLen=len(contactsB[0][6])
        for i in range(len(contactsA)):
            if i not in addedIs:
                tempAnnots=["A"]
                tempAnnots.extend(contactsA[i][6])
                for j in range(BannotLen):
                    tempAnnots.append(".")
                newPeaks.append([contactsA[i][:6],tempAnnots])
        for k in range(len(contactsB)):
            if k not in addedKs:
                tempAnnots=["B"]
                for j in range(AannotLen):
                    tempAnnots.append(".")
                tempAnnots.extend(contactsB[k][6])
                newPeaks.append([contactsB[k][:6],tempAnnots])
    if dashV:
        return [contactsA[i] for i in range(len(contactsA)) if i not in newPeaks]
    elif dashU:
        return [contactsA[i] for i in range(len(contactsA)) if i in addedIs]
    else:
        return newPeaks


# In[ ]:


def intersect2D(A,B,args,header):
    res=_overlap2D(A,B,args['v'],args['m'],args['mc'],args['u'],args['bA'],args['allA'],args['wo'],args['wa'],args['wb'],args['d'])

    if not args['v'] and not args['u']:
        res=_formatContacts(res,"\t")
    else:
        res=_formatContactsV(res,"\t")
        
    if __name__=="__main__": 
        try:
            if len(res)!=0:
                if len(header)!=0:
                    print(header)
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
    #parse args
    parser=argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
    parser.add_argument('-stdInA',help="Will use stdin for file a.  ", required=False,action='store_true')
    parser.add_argument('-b',help="File Path for file b.  Required for merge and intersect unless -stdInB is used", required=False,default="%#$")
    parser.add_argument('-stdInB',help="Will use stdin for file b.",action='store_true')
    parser.add_argument('-d',help="Specify  distance when searching for intersection.  Default 0",required=False,default=0,type=int)
    parser.add_argument('-v',help="Returns entries in A that do not overlap any entries in B.",action='store_true')
    parser.add_argument('-bA',help="Keep the annotations from file B instead of file A.",action='store_true')
    parser.add_argument('-allA',help="Keep the annotations from both files.  Annotations from A will come first.",action='store_true')
    parser.add_argument('-m',help="Returns the union of PGLs instead of the intersection of PGLs.",action='store_true')
    parser.add_argument('-mc',help="Returns only unions of PGLs where an overlap between files occurred",action='store_true')
    parser.add_argument('-u',help="Returns unique original entries from A where an intersection is found.",action='store_true')
    parser.add_argument('-wa',help="Returns the original PGLs from A if an intersection is found.",action='store_true')
    parser.add_argument('-wb',help="Returns the original PGLs from B if an intersection is found.",action='store_true')
    parser.add_argument('-wo',help="Returns the original PGLs, as well as the number of overlapping bases per anchor, if an intersection is found.",action='store_true')
    args = vars(parser.parse_args())

    #show help with no args
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #validate args
    if args['stdInB'] and args['stdInA']:
        print "stdin can only be used for either a or b"
        exit(1)
    elif args['stdInA']==False and args['a']=="%#$":
        print "either -stdInA or -a must be used"
        exit(1)
    elif args['stdInB']==False and args['b']=="%#$":
        print "either -stdInB or -b must be used"
        exit(1)
    if len([x for x in [args['v'],args['mc'],args['wa'],args['wb'],args['wo']] if x])>1:
        print "-v, -mc, -wa, -wb, and -wo cannot be used simulatneously."
        exit(1)
    if args['m'] and args['mc']:
        print "-m and -mc cannot be used simulatneously."
        exit(1)

    if args['stdInA']:
        header,A=processStdin()
    else:
        header,A=processFile(args['a'])

    if checkSorted(A)==1:
        print ("File A is not sorted.  Please use pgltools sort [FILE]")
        exit()
    elif checkSorted(A)==2:
        print ("File A is not a pgl file.  Please use pgltools formatbedpe [FILE]")
        exit()

    if args["b"]!="%#$":
        _,B=processFile(args['b'])
    if args['stdInB']:
        _,B=processStdin()

    if checkSorted(B)==1:
        print ("File B is not sorted.  Please use pgltools sort [FILE]")
        exit()
    elif checkSorted(B)==2:
        print ("File B is not a pgl file.  Please use pgltools formatbedpe [FILE]")
        exit()

    intersect2D(A,B,args,header)


