
# coding: utf-8

# In[ ]:

import argparse
import sys


# In[ ]:

parser=argparse.ArgumentParser()
parser._optionals.title = "Arguments"
parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
parser.add_argument('-stdInA',help="Use stdin for A", action='store_true')
args = vars(parser.parse_args())


# In[ ]:

if len(sys.argv)==1:
    print("Please provide a file to format")
    sys.exit(1)


# In[ ]:

if not args['stdInA']:
    for line in open(args['a'],"r"):
        if line[0]=="#":
            header="#chr\tstart\tstop\tAnchor_A_or_B\t"
            header+="\t".join(line.split()[6:])
            print header
        else:
            line=line.split()
            print ("\t".join(line[:3])+"\tA\t"+"\t".join(line[6:]))
            print ("\t".join(line[3:6])+"\tB\t"+"\t".join(line[6:]))
else:
    lines=[]
    for line in sys.stdin:
        if line[0]=="#":
            header="#chr\tstart\tstop\tAnchor_A_or_B\t"
            header+="\t".join(line.split()[6:])
            print header
        else:
            line=line.split()
            print "\t".join(line[:3])+"\tA\t"+"\t".join(line[6:])
            print "\t".join(line[3:6])+"\tB\t"+"\t".join(line[6:])


