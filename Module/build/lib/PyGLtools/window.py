
# coding: utf-8

# In[ ]:

import argparse
import sys
from pgltools_library import *


# In[ ]:

def _formatContacts(contacts,delim):
    return [delim.join([str(y) for y in x[:-1]])+delim+delim.join([str(y) for y in x[-1]]) for x in contacts]


# In[ ]:

def _filterOnWindow(contacts,window1,window2):
    # filter contactsA on window1 and contactsB on window2.  If one is not supplied, only filter on the one that is present
    if len(window1)==3 and len(window2)==3:
        contacts=[x for x in contacts if window1[0]==x[0] and window1[1]<=x[1] and window1[2]>=x[2] and window2[0]==x[3] and window2[1]<=x[4] and window2[2]>=x[5]]
    elif len(window1)==3 and len(window2)==0:
        contacts=[x for x in contacts if window1[0]==x[0] and window1[1]<=x[1] and window1[2]>=x[2]]
    elif len(window2)==3 and len(window1)==0:
        contacts=[x for x in contacts if window2[0]==x[3] and window2[1]<=x[4] and window2[2]>=x[5]]
    elif len(window1)==3 and len(window2)==1:
        contacts=[x for x in contacts if window1[0]==x[0] and window1[1]<=x[1] and window1[2]>=x[2] and window2[0]==x[3]]
    elif len(window2)==3 and len(window1)==1:
        contacts=[x for x in contacts if window2[0]==x[3] and window2[1]<=x[4] and window2[2]>=x[5] and window1[0]==x[0]]   
    elif len(window1)==1 and len(window2)==1:
        contacts=[x for x in contacts if window1[0]==x[0] and window2[0]==x[3]]
    elif len(window1)==1:
        contacts=[x for x in contacts if window1[0]==x[0]]
    elif len(window2)==1:
        contacts=[x for x in contacts if window2[0]==x[3]]
    return contacts


# In[ ]:

def window(A,args): 
    
    if "-" in args['window1'] and ":" in args['window1']:
        w1=[args['window1'].split(":")[0],int(args['window1'].split(":")[1].split("-")[0]),int(args['window1'].split(":")[1].split("-")[1])]
    elif args['window1']!="%#$":
        w1=[args['window1']]
    else:
        w1=[]
    if "-" in args['window2'] and ":" in args['window2']:
        w2=[args['window2'].split(":")[0],int(args['window2'].split(":")[1].split("-")[0]),int(args['window2'].split(":")[1].split("-")[1])]
    elif args['window2']!="%#$":
        w2=[args['window2']]
    else:
        w2=[]
        
    res=_filterOnWindow(A,w1,w2)
    res=_formatContacts(res,"\t")
    if __name__=="__main__":
        try:
            if len(res)!=0:
                if len(header)!=0:
                    print(header)
                print("\n".join(res))
        except IOError as e:
            if e.errno==32:
                exit()
    else:
        funcOut=[]
        for r in res:
            r=r.split("\t")
            funcOut.append([r[0],int(r[1]),int(r[2]),r[3],int(r[4]),int(r[5]),r[6:]])
        return funcOut


# In[ ]:

if __name__=="__main__":
    #parse args
    parser=argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
    parser.add_argument('-stdInA',help="Will use stdin for file a.", required=False,action='store_true')
    parser.add_argument('-window1',help="chrom:start-end, or just chrom.  Only 1 window is needed", required=False,default="%#$")
    parser.add_argument('-window2',help="chrom:start-end, or just chrom.  Only 1 window is needed", required=False,default="%#$")
    args = vars(parser.parse_args())

    #show help with no args
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #validate args
    if args['window1']=="" and args['window2']=="":
        print "Either window1, window2, or window1 and window2 must be provided"
        exit(1)
    if args['a']=="%#$" and args['stdInA']==False:
        print "Either a or stdInA must be used"
        exit(1)

    if args['stdInA']:
        header,A=processStdin()
    else:
        header,A=processFile(args['a'])

    window(A,args)


