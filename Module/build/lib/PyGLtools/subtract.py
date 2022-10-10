
# coding: utf-8

# In[ ]:


import argparse
import sys
from pgltools_library import *


# In[ ]:


def _formatContacts(contacts,delim):
    return [delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts]


# In[ ]:


def _overlap2D(contactsA,contactsB):
    #our files are going to be given with [chr1 binStart1 binEnd1 chr2 binStart2 binEnd2]
    i=0
    k=0
    restartK=-1
    maximalRestart=0
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

            if startA1 < startB1 and endA1 =< startB1:
                i+=1
                k=restartK
                continue
            elif startB1 < startA1 and endB1 <= startA1:
                if maximalRestart<=startA1: #should always ==, < is present for my sanity
                    restartK=k
                k+=1
                maximalRestart=0
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

                if startA2 < startB2 and endA2 <= startB2:
                    if k==len(contactsB)-1:
                        i+=1
                        k=restartK
                    else:
                        k+=1

                elif startB2 < startA2 and endB2 <= startA2:
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
    return newPeaks


# In[ ]:


def subtract2D(A,B,args,header):
    res=_overlap2D(A,B)
    res=_formatContacts(res,"\t")

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
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False)
    parser.add_argument('-stdInA',help="Will use stdin for file a.  ", required=False,action='store_true')
    parser.add_argument('-b',help="File Path for file b.  Required for merge and intersect unless -stdInB is used", required=False,default="%#$")
    parser.add_argument('-stdInB',help="Will use stdin for file b.",action='store_true')
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

    subtract2D(A,B,args,header)


