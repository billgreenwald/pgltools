
# coding: utf-8

# In[ ]:

import argparse
import sys


# In[ ]:

parser=argparse.ArgumentParser()
parser._optionals.title = "Arguments"
parser.add_argument('-ts',help="File Path of Triple Sparse matrix file.", required=True)
parser.add_argument('-an',help="File Path of annotation file.",required=True)
args = vars(parser.parse_args())


# In[ ]:

annotationMap={line.split()[3]:"\t".join(line.split()[:3]) for line in open(args['an'])}

for line in open(args['ts']):
    line=line.split()
    try:
        print (annotationMap[line[0]]+"\t"+annotationMap[line[1]]+"\t"+line[2])
    except IOError as e:
        if e.errno==32:
            exit()


