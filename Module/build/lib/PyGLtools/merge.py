
# coding: utf-8

# In[ ]:


import argparse
import sys
from pgltools_library import *


# In[ ]:


def _formatContacts(contacts,delim):
    if len(contacts[0])==6:
        return [delim.join([str(y) for y in x]) for x in contacts]
    else:
        return [delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts]


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
        originalOrder={}
        for i,x in enumerate(operatedOnList):
            if x not in originalOrder:
                originalOrder[x]=i
        return delim.join([str(x) for x in sorted(list(set(operatedOnList)),key=lambda x:originalOrder[x])])
    elif operation=="count":
        return max(1,len(operatedOnList))
    elif operation=="count_distinct":
        return (len(list(set(operatedOnList))))


# In[ ]:


def _merge(contacts,cols,commands,d):
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
                if startA1 < startB1-d and endA1 <= startB1-d:
                    j+=1
                    continue
                elif startB1 < startA1-d and endB1 <= startA1-d:
                    j+=1
                    continue
                else:
                    #the first bins overlap
                    if startA2 < startB2-d and endA2 <= startB2-d:
                        j+=1
                        continue
                    elif startB2 < startA2-d and endB2 <= startA2-d:
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
            if startA1 < startB1-d and endA1 <= startB1-d:
                advanceI=True
            elif startB1 < startA1-d and endB1 <= startA1-d:
                advanceI=True
            else:
                #the first bins overlap
                if startA2 < startB2-d and endA2 <= startB2-d:
                    advanceI=False
                elif startB2 < startA2-d and endB2 <= startA2-d:  #shouldnt happen due to sorting
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
    return [x if len(x[6])!=0 else [x[0],x[1],x[2],x[3],x[4],x[5],[x[6]]] for x in contacts]


# In[ ]:


def _processCommands(contacts,cols,commands,dashDelim):
    if len(cols)>0:
        for i in range(len(contacts)):
            newAnnot=[]
            for ind in range(len(cols)):
                if type(contacts[i][6][0])!=list and cols[ind]!=0:
                    newAnnot.append(_operation([contacts[i][6][cols[ind]-6]],commands[ind],dashDelim))
                else:
                    newAnnot.append(_operation(contacts[i][6][ind],commands[ind],dashDelim))

            contacts[i][6]=newAnnot
    else:
        contacts=[x[:6] for x in contacts]
    return contacts


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


def merge(A,args,header):
    if args['c']!="%#$":
        cols=[int(x) for x in args['c'].split(',')]
        commands=args['o'].split(',')
    else:
        cols=[]
        commands=[]

    if len(cols)>0:
        if max(cols)>6+len(A[0][-1]):
            print ("A -c argument surpassed the number of columns in the pgl file given")
            exit()

    res=_merge(A,[x-1 for x in cols],commands,args['d'])
    reMerge=_merge(sorted(res),[x-1 for x in cols],commands,args['d'])

    while len(res)!=len(reMerge):
        res=reMerge[:]
        reMerge=_merge(sorted(res),[x-1 for x in cols],commands,args['d'])


    res=_processCommands(res,[x-1 for x in cols],commands,args['delim'])
    res=_formatContacts(res,"\t")

    if __name__=="__main__": 
        useOld=False
        try:
            if len(res)!=0:
                if len(header)>0:
                    if len(header[0].split())>6+len(A[0][-1]):
                        useOld=True
                if not args['noH']:
                    print _createHeader(header.split(),cols,commands,useOld)
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
    parser.add_argument('-c',help="Specify Column for operation to be performed on.  Requires -o.  1 indexed", default="%#$",required=False)
    parser.add_argument('-o',help="Specify operation to be performed on column.  Requires -c.  1 indexed", required=False,default="%#$")
    parser.add_argument('-delim',help="Delimeter for -o collapse or -o distinct. Default \",\"", required=False,default=",")
    parser.add_argument('-d',help="Distance allowed between contacts for merging. Default 0", required=False,default=0,type=int)
    parser.add_argument('-noH',help="Skip generation of header from merge commands.", required=False,action='store_true')
    args = vars(parser.parse_args())

    #show help with no args
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #validate args
    if args['stdInA']==False and args['a']=="%#$":
        print "either -stdInA or -a must be used"
        exit(1)
    if args['o']=="%#$" and args['c']!="%#$":
        print "-c and -o must be used together"
        exit(1)
    if args['o']!="%#$" and args['c']=="%#$":
        print "-c and -o must be used together"
        exit(1)
    if len(args['c'].split(",")) != len(args['o'].split(",")):
        print "-c and -o must have the same number of arguments"
        exit(1)
    if not all([x in ["sum","min","max","absmin","absmax","mean","median","collapse","distinct","count","count_distinct", "%#$"] for x in args['o'].split(",")]):
        print "invalid operation given.  Valid operations are: sum, min, max, absmin, absmax, mean, median, collapse, distinct, count, count_distinct"
        exit(1)
    if args['d']<0:
        print "d must be positive"
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

    merge(A,args,header)


