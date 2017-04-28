
# coding: utf-8

# In[ ]:

import argparse
import sys
from pgltools_library import *


# In[ ]:

parser=argparse.ArgumentParser()
parser._optionals.title = "Arguments"
parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
parser.add_argument('-stdInA',help="Use stdin for A", action='store_true')
parser.add_argument('-N',help="Specify column for naming entry.  If not given, entries are named Contact_#", required=False,default=0,type=int)
parser.add_argument('-C',help="Specify column for coloring entry.  If not given, entries are all colored black.", required=False,default=0,type=int)
args = vars(parser.parse_args())


# In[ ]:

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)


# In[ ]:

if args['stdInA'] and args['a']!="%#$":
    print "-stdInA and -a cannot be used simultaneously"
    exit(1)
elif args['stdInA']==False and args['a']=="%#$":
    print "either -stdInA or -a must be used"
    exit(1)


# In[ ]:

def formatContacts(contacts,nameCol,colorCol):
    res=[]
    i=-1
    for contact in contacts:
        i+=1
        chromA=contact[0]
        startA=str(contact[1])
        stopA=str(contact[2])
        chromB=str(contact[3])
        startB=str(contact[4])
        stopB=str(contact[5])
        if nameCol!=-1:
            name=contact[6][nameCol-6]
        else:
            name="Contact_"+str(i)
        if colorCol!=-1:
            color=contact[6][scoreCol-6]
        else:
            color="0,0,0"
        res.append("\t".join([chromA,startA,stopA,chromB,startB,stopB,name,color]))
        
    return res


# In[ ]:

if args['stdInA']:
    _,A=processStdin()
else:
    _,A=processFile(args['a'])

minNumCols=min([6+len(y[-1]) for y in A])

if any([x<0 for x in [args["N"],args["C"]]]):
    print "Valid column numbers must be given.  Column numbering starts with 1"
    exit(1)
if any([x>minNumCols for x in [args["N"],args["C"]]]):
    print "A specified column exceeds the number of columns present in the file"
    exit(1)

res=formatContacts(A,args["N"]-1,args["C"]-1)

try:
    print("\t".join(["chr1","x1","x2","chr2","y1","y2","color","comment"]))
    print("\n".join(res))
except IOError as e:
    if e.errno==32:
        exit()


