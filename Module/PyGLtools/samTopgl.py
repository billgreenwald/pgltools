
# coding: utf-8

# In[ ]:

import argparse
import sys
import re
from pgltools_library import *


# In[ ]:

parser=argparse.ArgumentParser()
parser._optionals.title = "Arguments"
parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
parser.add_argument('-stdInA',help="Will use stdin for file a.  ", required=False,action='store_true')
parser.add_argument('-delim',help="Read end delimeter.  default \"/\"", required=False,default="/")
parser.add_argument('-ins',help="Insert size of library sequencing.  Functions as an upper bound on split read distance. Default 1000 bp",required=False,type=int,default=1000)
args = vars(parser.parse_args())


# In[ ]:

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)


# In[ ]:

elif args['stdInA']==False and args['a']=="%#$":
    print "either -stdInA or -a must be used"
    exit(1)


# In[2]:

def formatContacts(contacts):
    return ["\t".join([str(y) for y in x]) for x in contacts]


# In[ ]:

def processRead(name,chrom,start,length,cigar,flipped):
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


# In[3]:

def samTopglStdIn(delim,insertSize):
    #reads are stored as name,chrom,start,end
    reads=[]
    contacts=[]
    header=""
    for line in sys.stdin:
        if line[0]=="#":
            header+=line.strip()+"\n"
            continue
        line=line.split()
        if len(reads)==0:
            if line[1]=="16":
                reads.append(processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],True))
            else:
                reads.append(processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],False))
        elif reads[-1][0].split(delim)[0]==line[0].split(delim)[0]:
            if line[1]=="16":
                reads.append(processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],True))
            else:
                reads.append(processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],False))
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
                        chrB=groupedReads[chroms[1]][0][1]
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
    
    return header,contacts


# In[ ]:

def samTopgl(samfile,delim,insertSize):
    #reads are stored as name,chrom,start,end
    reads=[]
    contacts=[]
    header=""
    for line in open(samfile,"r"):
        if line[0]=="#":
            header+=line.strip()+"\n"
            continue
        line=line.split()
        if len(reads)==0:
            if line[1]=="16":
                reads.append(processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],True))
            else:
                reads.append(processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],False))
        elif reads[-1][0].split(delim)[0]==line[0].split(delim)[0]:
            if line[1]=="16":
                reads.append(processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],True))
            else:
                reads.append(processRead(line[0],line[2],int(line[3]),len(line[9]),line[5],False))
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
    
    return header,contacts


# In[14]:

if args['stdInA']:
    header,res=samTopglStdIn(args['delim'],args['ins'])
else:
    header,res=samTopgl(args['a'],args['delim'],args['ins'])

res=formatContacts(res)

try:
    if len(header)!=0:
        print(header)
    print("\n".join(res))
except IOError as e:
    if e.errno==32:
        exit()


