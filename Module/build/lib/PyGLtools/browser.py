
# coding: utf-8

# In[ ]:

import argparse
import sys
from pgltools_library import *


# In[ ]:

def formatForBrowser(contacts,nameCol,scoreCol,pCol,qCol,colorCol):
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
            name=chrom+":"+str(contact[1])+".."+str(contact[2])+"-"+chrom+":"+str(contact[4])+".."+str(contact[5])
        if scoreCol!=-1:
            score=contact[6][scoreCol-6]
        else:
            score="1000"
        strand="."
        thickStart="0"
        thickEnd="0"
        if colorCol!=-1:
#             rgb=contact[6][colorCol-6]
            rgs="0"
        else:
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

def browser(A,N=0,S=0,P=0,Q=0,tN='pgl_track',C=0):
    """Takes a PyGL formatted list A and returns a UCSC genome browser formatted bed12 file."""
    minNumCols=min([6+len(y[-1]) for y in A])

    if any([x<6 and x!=0 for x in [N,S,P,Q,C]]):
        print "Valid column numbers must be given.  Column numbering starts with 1.  The 6 required PGL columns cannot be used."
        if __name__!="__main__":
            exit(1)
        else:
            return
    if any([x>minNumCols for x in [N,S,P,Q,C]]):
        print "A specified column exceeds the number of columns present in the file"
        if __name__!="__main__":
            exit(1)
        else:
            return

    res=formatForBrowser(A,N-1,S-1,P-1,Q-1,C-1)
    if __name__=="__main__":
        try:
            print("track name="+tN+" type=gappedPeak")
            print("\n".join(res))
        except IOError as e:
            if e.errno==32:
                exit()
    else:
        funcOut=""
        funcOut+="track name="+tN+" type=gappedPeak"
        funcOut+="\n".join(res)
        return funcOut
                
    
#     else:
#         funcOut=[]
#         for r in res:
#             r=r.split("\t")
#             funcOut.append([r[0],int(r[1]),int(r[2]),r[3],int(r[4]),int(r[5]),r[6:]])
#         return funcOut


# In[ ]:

if __name__=="__main__":

    #get command line arguments
    parser=argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
    parser.add_argument('-stdInA',help="Use stdin for A", action='store_true')
    parser.add_argument('-N',help="Specify column for naming entry.  If not given, entries are named Contact_#", required=False,default=0,type=int)
    parser.add_argument('-S',help="Specify column for scoring entry.  If not given, entries are scored uniformly", required=False,default=0,type=int)
    parser.add_argument('-C',help="Specify column for coloring entry.  If not given, entries are colored black", required=False,default=0,type=int)
    parser.add_argument('-P',help="Specify column for pValue of entry.  If not given, pValue is ignored", required=False,default=0,type=int)
    parser.add_argument('-Q',help="Specify column for qValue of entry.  If not given, qValue is ignored", required=False,default=0,type=int)
    parser.add_argument('-tN',help="Track name. If not given, track is named \"pgl_track\"", required=False,default="pgl_track")
    args = vars(parser.parse_args())

    #print help if no arguments given
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #validate arguments
    if args['stdInA'] and args['a']!="%#$":
        print "-stdInA and -a cannot be used simultaneously"
        exit(1)
    elif args['stdInA']==False and args['a']=="%#$":
        print "either -stdInA or -a must be used"
        exit(1)
        
    if args['stdInA']:
        _,A=processStdin()
    else:
        _,A=processFile(args['a'])

    browser(A,N=args['N'],S=args['S'],P=args['P'],Q=args['Q'],tN=args['tN'],C=args['C'])


