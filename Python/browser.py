
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
parser.add_argument('-S',help="Specify column for scoring entry.  If not given, entries are scored uniformly", required=False,default=0,type=int)
parser.add_argument('-P',help="Specify column for pValue of entry.  If not given, pValue is ignored", required=False,default=0,type=int)
parser.add_argument('-Q',help="Specify column for qValue of entry.  If not given, qValue is ignored", required=False,default=0,type=int)
parser.add_argument('-tN',help="Track name. If not given, track is named \"be2d_track\"", required=False,default="be2d_track")
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

def formatContacts(contacts,nameCol,scoreCol,pCol,qCol):
    res=[]
    i=-1
    for contact in contacts:
        i+=1
        if contact[0]!=contact[3]:
            continue
        chrom=contact[0]
        start=str(contact[1])
        end=str(contact[5])
        if nameCol!=-1:
            name=contact[6][nameCol-6]
        else:
            name="chr:"+str(contact[1])+".."+str(contact[2])+"-chr:"+str(contact[4])+".."+str(contact[5])
        if scoreCol!=-1:
            score=contact[6][scoreCol-6]
        else:
            score="1000"
        strand="."
        thickStart="0"
        thickEnd="0"
        rgb="0"
        blockCount="2"
        blockSizes=str(contact[2]-contact[1])+","+str(contact[5]-contact[4])
        blockStarts="0,"+str(contact[4]-contact[1])
        signalValue="0"
        if pCol!=-1:
            pValue=contact[6][pCol-6]
        else:
            pValue="0"
        if qCol!=-1:
            qValue=contact[6][qCol-6]
        else:
            qValue="0"
        
        res.append("\t".join([chrom,start,end,name,score,strand,thickStart,thickEnd,rgb,blockCount,blockSizes,blockStarts,signalValue,pValue,qValue]))
        
    return res


# In[ ]:

if args['stdInA']:
    _,A=processStdin()
else:
    _,A=processFile(args['a'])

minNumCols=min([6+len(y[-1]) for y in A])

if any([x<0 for x in [args["N"],args["S"],args["P"],args["Q"]]]):
    print "Valid column numbers must be given.  Column numbering starts with 1"
    exit(1)
if any([x>minNumCols for x in [args["N"],args["S"],args["P"],args["Q"]]]):
    print "A specified column exceeds the number of columns present in the file"
    exit(1)

res=formatContacts(A,args["N"]-1,args["S"]-1,args["P"]-1,args["Q"]-1)

print("track name="+args['tN']+" type=gappedPeak")
print("\n".join(res))


