
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
parser.add_argument('-d',help="Distance to expand by", required=False,default=0,type=int)
parser.add_argument('-g',help="path to genome file.  file should be two columns tab separated: the first is chromosome name, the second is chromosome length", required=False,default="%#$")
args = vars(parser.parse_args())


# In[ ]:

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)


# In[ ]:

if args['a']=="%#$" and args['stdInA']==False:
    print "Either a or stdInA must be used"
    exit(1)


# In[ ]:

def formatContacts(contacts,delim):
    return [delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts]


# In[ ]:

def processGenome(genomeFile):
    lines=[line.strip().split() for line in open(genomeFile,"r")]
    if len([x for x in lines if len(x)!=2 and len(x) !=0])!=0:
        print "Genome file has more than 2 columns"
        exit()
    return {x[0]:int(x[1]) for x in lines if len(x)==2}


# In[ ]:

def expand(contacts,d,genome):
    missing=set()
    if len(genome)!=0:
        for contact in contacts:
            contact[1]=max(0,contact[1]-d)
            contact[4]=max(0,contact[4]-d)
            if contact[0] in genome:
                contact[2]=min(genome[contact[0]],contact[2]+d)
            else:
                if contact[0] not in missing:
                    sys.stderr.write(contact[0]+" is not found in the genome file.")
                    missing.add(contact[0])
                contact[2]=contact[2]+d
            if contact[3] in genome:
                contact[5]=min(genome[contact[3]],contact[5]+d)
            else:
                if contact[3] not in missing:
                    sys.stderr.write(contact[3]+" is not found in the genome file.")
                    missing.add(contact[3])
                contact[5]=contact[5]+d
            
    else:
        for contact in contacts:
            contact[1]=max(0,contact[1]-d)
            contact[2]=contact[2]+d
            contact[4]=max(0,contact[4]-d)
            contact[5]=contact[5]+d
    
    return contacts


# In[ ]:

if args['stdInA']:
    header,A=processStdin()
else:
    header,A=processFile(args['a'])
        
if args['g']!="%#$":
    genome=processGenome(args['g'])
else:
    genome={}
res=expand(A,args['d'],genome)
res=formatContacts(res,"\t")

if len(res)!=0:
    if len(header)!=0:
        print(header)
    try:
        print("\n".join(res))
    except IOError as e:
        if e.errno==32:
            exit()


