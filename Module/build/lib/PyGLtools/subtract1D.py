
# coding: utf-8

# In[ ]:


import argparse
import sys
from pgltools_library import *


# In[ ]:


def _formatContacts(contacts,delim):
    return [delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts if len(x)!=0]


# In[ ]:


def _subtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,whichBin):
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


def _overlap1D(contactsA,bedB):
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
                    startB=bedB[chrB][k][0]
                    endB=bedB[chrB][k][1]
                    if startB!=endB:
                        startB+=1

                    if startA1 < startB and endA1 <= startB:
                        pass
                    elif startB < startA1 and endB <= startA1:
                        pass
                    else:
                        newPeaks.extend(_subtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,1))

                    if startA2 < startB and endA2 < startB:
                        pass
                    elif startB < startA2 and endB < startA2:
                        pass
                    else:
                        newPeaks.extend(_subtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,2))


        else:
            if chrA1 in bedB:
                for k in range(len(bedB[chrA1])):
                    chrB=chrA1
                    startB=bedB[chrB][k][0]
                    endB=bedB[chrB][k][1]
                    if startB!=endB:
                        startB+=1

                    if startA1 < startB and endA1 <= startB:
                        continue
                    elif startB < startA1 and endB <= startA1:
                        break
                    else:
                        newPeaks.extend(_subtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,1))

            if chrA2 in bedB:
                for k in range(len(bedB[chrA2])):
                    chrB=chrA2
                    startB=bedB[chrB][k][0]
                    endB=bedB[chrB][k][1]
                    if startB!=endB:
                        startB+=1

                    if startA2 < startB and endA2 <= startB:
                        continue
                    elif startB < startA2 and endB <= startA2:
                        break
                    else:
                        newPeaks.extend(_subtract1D(chrA1,startA1,endA1,chrA2,startA2,endA2,chrB,startB,endB,Aannots,2))
                
    return newPeaks


# In[ ]:


def subtract1D(A,B,args,header):
    res=_overlap1D(A,B)
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
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
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
        _,B=processBedFile(args['b'])
    if args['stdInB']:
        _,B=processStdinBed()


    subtract1D(A,B,args,header)


