
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

def findLoops(contacts):
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
        annots="\t".join(contact[6])
        if chromA==chromB:
            res.append("\t".join([chromA,startA,stopB,annots]))
        else:
            res.append("\t".join([chromA,startA,stopA,annots]))
            res.append("\t".join([chromB,startB,stopB,annots]))
        
    return res


# In[ ]:

if args['stdInA']:
    _,A=processStdin()
else:
    _,A=processFile(args['a'])

res=findLoops(A)

print("\n".join(res))


