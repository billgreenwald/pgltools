
# coding: utf-8

# In[ ]:

import argparse
import sys


# In[ ]:

def _condense(args):
    if not args['stdInA']:
        for line in open(args['a'],"r"):
            if line[0]=="#":
                header="#chr\tstart\tstop\tAnchor_A_or_B\t"
                header+="\t".join(line.split()[6:])
                print header
            else:
                line=line.split()
                try:
                    print "\t".join(line[:3])+"\tA\t"+"\t".join(line[6:])
                    print "\t".join(line[3:6])+"\tB\t"+"\t".join(line[6:])
                except IOError as e:
                    if e.errno==32:
                        exit()
    else:
        lines=[]
        for line in sys.stdin:
            if line[0]=="#":
                header="#chr\tstart\tstop\tAnchor_A_or_B\t"
                header+="\t".join(line.split()[6:])
                print header
            else:
                line=line.split()
                try:
                    print "\t".join(line[:3])+"\tA\t"+"\t".join(line[6:])
                    print "\t".join(line[3:6])+"\tB\t"+"\t".join(line[6:])
                except IOError as e:
                    if e.errno==32:
                        exit()


# In[ ]:

def condense(A,asObject=False):
    if not asObject:
        funcOut=""
        for line in A:
            funcOut+="\t".join(line[:3])+"\tA\t"+"\t".join(line[6:]) + "\n"
            funcOut+="\t".join(line[3:6])+"\tB\t"+"\t".join(line[6:]) + "\n"
    else:
        funcOut={}
        for line in A:
            if line[0] not in funcOut:
                funcOut[line[0]]=[]
            if line[3] not in funcOut:
                funcOut[line[3]]=[]
            funcOut[line[0]].append([int(line[1]),int(line[2]),line[6:]])
            funcOut[line[3]].append([int(line[4]),int(line[5]),line[6:]])
    return funcOut


# In[ ]:

if __name__=="__main__":
    
    #parse args
    parser=argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
    parser.add_argument('-stdInA',help="Use stdin for A", action='store_true')
    args = vars(parser.parse_args())

    #validate args
    if len(sys.argv)==1:
        print("Please provide a file to format")
        sys.exit(1)
    
    _condense(args)


