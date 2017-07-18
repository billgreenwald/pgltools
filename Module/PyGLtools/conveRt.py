
# coding: utf-8

# In[ ]:

import argparse
import sys
from pgltools_library import *


# In[ ]:

def _formatForConvert(contacts,countCol,pCol,qCol):
    res=[]
    i=-1
    for contact in contacts:
        if countCol!=-1:
            count=contact[6][countCol-6]
        else:
            count="0"
        if pCol!=-1:
            pValue=contact[6][pCol-6]
        else:
            pValue="0"
        if qCol!=-1:
            qValue=contact[6][qCol-6]
        else:
            qValue="0"
        
        res.append("\t".join([contact[0],str(contact[1]),str(contact[2]),contact[3],str(contact[4]),str(contact[5]),count,pValue,qValue]))
        
    return res


# In[ ]:

def conveRt(A,args):
    minNumCols=min([6+len(y[-1]) for y in A])

    if any([x<6 and x!=0 for x in [args["C"],args["P"],args["Q"]]]):
        print "Valid column numbers must be given.  Column numbering starts with 1.  Cannot use required PGL column."
        exit(1)
    if any([x>minNumCols for x in [args["C"],args["P"],args["Q"]]]):
        print "A specified column exceeds the number of columns present in the file"
        exit(1)

    res=_formatForConvert(A,args["C"]-1,args["P"]-1,args["Q"]-1)

    if __name__=="__main__":
        if len(res)!=0:
            try:
                print("chromA\tstartA\tstopA\tchromB\tstartB\tstopB\tcount\tpValue\tqValue")
                print("\n".join(res))
            except IOError as e:
                if e.errno==32:
                    exit()
    else:
        funcOut=""
        funcOut+="chromA\tstartA\tstopA\tchromB\tstartB\tstopB\tcount\tpValue\tqValue"
        funcOut+="\n".join(res)
        return funcOut


# In[ ]:

if __name__=="__main__":
    #parse args
    parser=argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
    parser.add_argument('-stdInA',help="Use stdin for A", action='store_true')
    parser.add_argument('-C',help="Specify column for read count.  If not given, count is set to 0", required=False,default=0,type=int)
    parser.add_argument('-P',help="Specify column for pValue of entry.  If not given, pValue is set to 0", required=False,default=0,type=int)
    parser.add_argument('-Q',help="Specify column for qValue of entry.  If not given, qValue is set to 0", required=False,default=0,type=int)
    args = vars(parser.parse_args())

    #display help with no args
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #validate args
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

    conveRt(A,args)
    


