
# coding: utf-8

# In[1]:


import argparse
import sys
from pgltools_library import *


# In[ ]:


def _formatContacts(contacts,delim):
    return [delim.join([str(y) for y in x[0]])+delim+delim.join([str(y) for y in x[1]]) for x in contacts]


# In[27]:


def _overlap1D(contactsA,bedB,useBAnnots,useAllAnnots,aLocations,dist,dashV,reportBasAnnot,dashU):
    #we will hash the bed file for instant lookup
    if dashV or dashU:
        intersectedContactIndicies=set()
    newPeaks=[]
    #compare file 2 to file 1, meaning advance file 2 first
    for i in range(len(contactsA)): 
            chrA1=contactsA[i][0]
            startA1=max(contactsA[i][1],0)
            endA1=contactsA[i][2]
            chrA2=contactsA[i][3]
            startA2=max(contactsA[i][4],0)
            endA2=contactsA[i][5]
            difChrom=False
            
            if chrA1==chrA2:
                if chrA1 in bedB:
                    for k in range(len(bedB[chrA1])): 
                        Aannots=contactsA[i][6][:]

                        chrB=chrA1
                        startB=bedB[chrB][k][0]
                        endB=bedB[chrB][k][1]
                        if startB!=endB:
                            startB+=1
                        Bannots=bedB[chrB][k][2]

                        overlapA=False
                        overlapB=False
                        if startA1 < startB-dist and endA1 <= startB-dist:
                            pass
                        elif startB-dist < startA1 and endB+dist <= startA1:
                            pass
                        else:
                            overlapA=True

                        if startA2 < startB-dist and endA2 <= startB-dist:
                            pass
                        elif startB-dist < startA2 and endB+dist <= startA2:
                            pass
                        else:
                            overlapB=True

                        if overlapA and overlapB:
                            if dashV or dashU:
                                intersectedContactIndicies.add(i)
                                break
                            else:
                                if not aLocations:
                                    chr1=str(chrA1)
                                    start1=str(max(startA1,startB))
                                    end1=str(min(endA1,endB))
                                    start2=str(max(startA2,startB))
                                    end2=str(min(endA2,endB))
                                    chr2=str(chrA2)
                                else:
                                    chr1=chrA1
                                    start1=startA1
                                    end1=endA1
                                    chr2=chrA2
                                    start2=startA2
                                    end2=endA2
                                if useBAnnots:
                                    if reportBasAnnot:
                                        t="\t".join([str(chrB),str(startB-1),str(endB)])
                                        if t not in Bannots:
                                             Bannots.append(t)
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A,B"],Bannots])
                                elif useAllAnnots:
                                    for ann in Bannots:
                                        Aannots.append(ann)
                                    if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A,B"],Aannots])
                                else:
                                    if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A,B"],Aannots])

                        elif overlapA:
                            if dashV or dashU:
                                intersectedContactIndicies.add(i)
                                break
                            else:
                                if not aLocations:
                                    chr1=str(chrA1)
                                    start1=str(max(startA1,startB))
                                    end1=str(min(endA1,endB))
                                else:
                                    chr1=chrA1
                                    start1=startA1
                                    end1=endA1
                                chr2=chrA2
                                start2=startA2
                                end2=endA2
                                if useBAnnots:
                                    if reportBasAnnot:
                                        t="\t".join([str(chrB),str(startB-1),str(endB)])
                                        if t not in Bannots:
                                             Bannots.append(t)
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Bannots])
                                elif useAllAnnots:
                                    for ann in Bannots:
                                        Aannots.append(ann)
                                    if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Aannots])
                                else:
                                    if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Aannots])

                        elif overlapB:
                            if dashV or dashU:
                                intersectedContactIndicies.add(i)
                                break
                            else:
                                chr1=chrA1
                                start1=startA1
                                end1=endA1
                                if not aLocations:
                                    start2=str(max(startA2,startB))
                                    end2=str(min(endA2,endB))
                                    chr2=str(chrA2)
                                else:
                                    chr2=chrA2
                                    start2=startA2
                                    end2=endA2
                                if useBAnnots:
                                    if reportBasAnnot:
                                        t="\t".join([str(chrB),str(startB-1),str(endB)])
                                        if t not in Bannots:
                                             Bannots.append(t)
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Bannots])
                                elif useAllAnnots:
                                    for ann in Bannots:
                                        Aannots.append(ann)
                                    if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Aannots])
                                else:
                                    if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                    newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Aannots])

            else:
                if chrA1 in bedB:
                    for k in range(len(bedB[chrA1])):
                        Aannots=contactsA[i][6][:]
                        chrB=chrA1
                        startB=max(bedB[chrB][k][0],0)
                        endB=bedB[chrB][k][1]
                        if startB!=endB:
                            startB+=1
                        Bannots=bedB[chrB][k][2]

                        difChrom=True
                        if startA1 < startB-dist and endA1 <= startB-dist:
                            continue
                        elif startB-dist < startA1 and endB+dist <= startA1:
                            break
                        else:
                            if dashV or dashU:
                                intersectedContactIndicies.add(i)
                                break
                            if not aLocations:
                                chr1=str(chrA1)
                                start1=str(max(startA1,startB))
                                end1=str(min(endA1,endB))
                            else:
                                chr1=chrA1
                                start1=startA1
                                end1=endA1
                            chr2=chrA2
                            start2=startA2
                            end2=endA2
                            if useBAnnots:
                                if reportBasAnnot:
                                        t="\t".join([str(chrB),str(startB-1),str(endB)])
                                        if t not in Bannots:
                                             Bannots.append(t)
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Bannots])
                            elif useAllAnnots:
                                for ann in Bannots:
                                    Aannots.append(ann)
                                if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Aannots])
                            else:
                                if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"A"],Aannots])
                if chrA2 in bedB:    
                    for k in range(len(bedB[chrA2])):
                        Aannots=contactsA[i][6][:]
                        chrB=chrA2
                        startB=max(bedB[chrB][k][0],0)
                        endB=bedB[chrB][k][1]
                        if startB!=endB:
                            startB+=1
                        Bannots=bedB[chrB][k][2]

                        if startA2 < startB-dist and endA2 <= startB-dist:
                            continue
                        elif startB-dist < startA2 and endB+dist <= startA2:
                            break
                        else:
                            if dashV or dashU:
                                intersectedContactIndicies.add(i)
                                break
                            chr1=chrA1
                            start1=startA1
                            end1=endA1
                            if not aLocations:
                                start2=str(max(startA2,startB))
                                end2=str(min(endA2,endB))
                                chr2=str(chrA2)
                            else:
                                chr2=chrA2
                                start2=startA2
                                end2=endA2
                            if useBAnnots:
                                if reportBasAnnot:
                                        t="\t".join([str(chrB),str(startB-1),str(endB)])
                                        if t not in Bannots:
                                             Bannots.append(t)
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Bannots])
                            elif useAllAnnots:
                                for ann in Bannots:
                                    Aannots.append(ann)
                                if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Aannots])
                            else:
                                if reportBasAnnot:
                                        Aannots.append("\t".join([str(chrB),str(startB-1),str(endB)]))
                                newPeaks.append([[chr1,start1,end1,chr2,start2,end2,"B"],Aannots])
    if not dashV and not dashU:            
        return newPeaks
    else:
        if dashV:
            return [[contactsA[i][:6],contactsA[i][6]] for i in range(len(contactsA)) if i not in intersectedContactIndicies]
        elif dashU:
            return [[contactsA[i][:6],contactsA[i][6]] for i in range(len(contactsA)) if i in intersectedContactIndicies]


# In[1]:


def intersect1D(A,B,args,header,headerB):
    res=_overlap1D(A,B,args['bA'],args['allA'],args['wa'],args['d'],args['v'],args['wb'],args['u'])
    res=_formatContacts(res,"\t")

    if __name__=="__main__":
        try:
            if len(res)!=0:
                if args['bA']:
                    if len(headerB)!=0:
                        wholeHeaderB=headerB.split("\n")
                        headerB=wholeHeaderB[-1].split("\t")
                        part2=headerB[6:]
                        headerB=headerB[:6]
                        headerB.append(args['anchA'])
                        headerB.extend(part2)
                        wholeHeaderB[-1]="\t".join(headerB)
                        print ("\n".join(wholeHeaderB))
                elif args['allA']:
                    if len(headerB)!=0 and len(header)!=0:
                        headerB=headerB.split("\n")
                        header=header.split("\n")

                        ht=header[0].split("\t")
                        ht2=ht[6:]
                        ht=ht[:6]
                        ht.append(args['anchA'])
                        ht.extend(ht2)
                        header[0]='\t'.join(ht)

                        headerB[0]=headerB[0][1:]

                        ht=headerB[0].split("\t")[3:]
                        if args['wb']:
                            ht.extend(['chr','start','end'])
                        headerB[0]='\t'.join(ht)

                        i=0
                        while i < len(headerB) or i < len(header):
                            if i < len(header) and i < len(headerB):
                                print(header[i]+"\t"+headerB[i])
                            elif i < len(header):
                                print(header[i])
                            else:
                                print(headerB[i])
                            i+=1
                    elif len(headerB)!=0:
                        print headerB
                    elif len(header)!=0:
                        header=header.strip().split()
                        t=header[:6]
                        t.append(args['anchA'])
                        t.extend(header[6:])
                        print("\t".join(t))
                else:
                    if len(header)!=0:
                        header=header.strip().split()
                        t=header[:6]
                        t.append(args['anchA'])
                        t.extend(header[6:])
                        print("\t".join(t))
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


# In[2]:


if __name__=="__main__":
    #parse arguments
    parser=argparse.ArgumentParser()
    parser._optionals.title = "Arguments"
    parser.add_argument('-a',help="File Path for file a.  Required unless -stdInA is used", required=False,default="%#$")
    parser.add_argument('-stdInA',help="Will use stdin for file a.  ", required=False,action='store_true')
    parser.add_argument('-b',help="File Path for file b.  Required for merge and intersect unless -stdInB is used", required=False,default="%#$")
    parser.add_argument('-stdInB',help="Will use stdin for file b.",action='store_true')
    parser.add_argument('-bA',help="Keep the annotations from the bed file instead of the pgl file.",action='store_true')
    parser.add_argument('-allA',help="Keep the annotations from the bed file as well as the pgl file.",action='store_true')
    parser.add_argument('-wa',help="Output original PGL rather than intersection when a region is found.",action='store_true')
    parser.add_argument('-wb',help="Output the original bed entry after each PGL entry it overlaps.",action='store_true')
    parser.add_argument('-v',help="Output PGLs that do not overlap any regions in the bed file.",action='store_true')
    parser.add_argument('-u',help="Output a PGL once if it overlaps any regions in the bed file.",action='store_true')
    parser.add_argument('-d',help="Distance for finding overlaps.  Default is 0",required=False,default=0,type=int)
    parser.add_argument('-anchA',help="Anchor intersection annotation for header.  Default is \"Intersected_Anchor\"",required=False,default='Intersected_Anchor',type=str)
    args = vars(parser.parse_args())

    #show help with no args
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    #validate args
    if args['stdInB'] and args['stdInA']:
        print "stdin can only be used for either a or b"
        exit(1)
    if args['stdInA']==False and args['a']=="%#$":
        print "either -stdInA or -a must be used"
        exit(1)
    if args['stdInB']==False and args['b']=="%#$":
        print "either -stdInB or -b must be used"
        exit(1)
    if args['bA']==True and args['allA']==True:
        print "-bA and -allA cannot be used at the same time"
        exit(1)
    if args['v']==True and args['u']==True:
        print "-v and -u cannot be used at the same time"
        exit(1)

    if args['stdInA']:
        header,A=processStdin()
    else:
        header,A=processFile(args['a'])

    if checkSorted(A)==1:
        print ("File A is not sorted.  Please use pgltools sort [FILE]")
        exit()
    elif checkSorted(A)==2:
        print ("File A is not a pgl file.  Please use pgltools formatbedpe [FILE]")
        exit()

    if args["b"]!="%#$":
        headerB,B=processBedFile(args['b'])
    if args['stdInB']:
        headerB,B=processStdinBed()

    intersect1D(A,B,args,header,headerB)


