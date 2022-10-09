
# coding: utf-8

# In[2]:

import browser as _brow
import closest as _clos2d
import closest1D as _clos1d
import condense as _cond
import conveRt as _conv
import coverage as _cov
import expand as _expa
import findLoops as _fl
import intersect as _inter2d
import intersect1D as _inter1d
import juicebox as _jb
import merge as _mer
import subtract as _subtr2d
import subtract1D as _subtr1d
import window as _wind
import pgltools_library as _pgltl
del pgltools_library


# In[1]:

def read_PGL(FilePath):
    """Takes a file path and returns a header and PyGL object of the pgl file.  Recommended use is header,pgl=read_PGL(FilePath)"""
    return _pgltl.processFile(FilePath)


# In[ ]:

def read_Bed(FilePath):
    """Takes a file path and returns a header and PyGL-bed object of the pgl file.  Recommended use is header,pgl=read_PGL(FilePath)"""
    return _pgltl.processBedFile(FilePath)


# In[ ]:

def _cs(pgl):
    return _pgltl.checkSorted(pgl)


# In[56]:

def pyglSort(PGL):
    """Takes a PyGL object and returns a sorted PyGL object"""
    return sorted(PGL,key=lambda x:(x[0],x[1],x[2],x[3],x[4],x[5]))


# In[2]:

def browser(PGL,N=0,S=0,P=0,Q=0,tN='pgl_track'):
    """Takes a PyGL object and returns a string formatted for the UCSC genome browser."""
    return _brow.browser(PGL,N,S,P,Q,tN)


# In[3]:

def closest1D(PGL,BED,ba=False):
    """Takes a PyGL object and a PyGL-bed object and returns a PyGL object resulting from the closest1D operation"""
    args={'ba':ba}
    return _clos1d.closest1D(PGL,BED,args)


# In[4]:

def closest2D(A,B):
    """Takes two PyGL objects and returns a PyGL object resulting from the closest operation"""
    return _clos2d.closest2D(A,B)


# In[72]:

def condense(PGL,asObject=False):
    """Takes a PyGL object and returns a string or PyGL-bed object resulting from the condense operation"""
    t=[]
    for i in range(len(PGL)):
        t1=[str(y) for y in PGL[i][:6]]
        t1.extend([str(y) for y in PGL[i][6]])
        t.append(t1)
    return _cond.condense(t,asObject=asObject)


# In[6]:

def conveRt(PGL,C=0,P=0,Q=0):
    """Takes a PyGL object and returns a string formatted by the conveRt operation"""
    args={'C':C,'P':0,'Q':0}
    return _conv.conveRt(PGL,args)


# In[7]:

def coverage(A,B,z=False):
    """Takes two PyGL objects and returns a PyGL object resulting from the coverage operation"""
    if _cs(A)!=0:
        print "A is not sorted.  Please use a pyglSort."
        return
    if _cs(B)!=0:
        print "B is not sorted.  Please use a pyglSort."
        return
    args={'z':z}
    return _cov.coverage(A,B,"",args)


# In[8]:

def expand(PGL,d=0,genome={}):
    """Takes a PyGL object and returns a PyGL object resulting from the expand operation"""
    args={'d':d}
    return _expa.expand(PGL,args,genome)


# In[9]:

def findLoops(PGL):
    """Takes a PyGL object and returns a PyGL-bed object resulting from the findLoops operation"""
    return _fl.findLoops(PGL)


# In[10]:

def intersect2D(A,B,d=0,v=False,bA=False,allA=False,m=False,mc=False,u=False,wa=False,wb=False,wo=False):
    """Takes two PyGL objects and returns a PyGL object resulting from the intersect operation"""
    if _cs(A)!=0:
        print "A is not sorted.  Please use a pyglSort."
        return
    if _cs(B)!=0:
        print "B is not sorted.  Please use a pyglSort."
        return
    args={'d':d,'v':v,'bA':bA,'allA':allA,'m':m,'mc':mc,'u':u,'wa':wa,'wb':wb,'wo':wo}
    return _inter2d.intersect2D(A,B,args,"")


# In[11]:

def intersect1D(PGL,BED,bA=False,allA=False,wa=False,wb=False,v=False,u=False,d=0):
    """Takes a PyGL object and a PyGL-bed object and returns a PyGL object resulting from the intersect1D operation"""
    if _cs(PGL)!=0:
        print "The PyGL supplied is not sorted.  Please use a pyglSort."
        return
    args={'bA':bA,'allA':allA,'wa':wa,'wb':wb,'v':v,'u':u,'d':d,}
    return _inter1d.intersect1D(PGL,BED,args,"","")


# In[12]:

def juicebox(PGL,N=0,C=0):
    """Takes a PyGL object and returns a string formatted by the juicebox operation"""
    args={'N':N,'C':C}
    return _jb.juicebox(PGL,args)


# In[13]:

def merge(PGL,c="%#$",o="%#$",delim=',',d=0):
    """Takes a PyGL object and returns a PyGL object resulting from the merge operation"""
    if _cs(PGL)!=0:
        print "The PyGL supplied is not sorted.  Please use a pyglSort."
        return
    args={'c':c,'o':o,'delim':delim,'d':d,'noH':True}
    return _mer.merge(PGL,args,"")


# In[35]:

def subtract2D(A,B):
    """Takes two PyGL objects and returns a PyGL object resulting from the subtract operation"""
    if _cs(A)!=0:
        print "A is not sorted.  Please use a pyglSort."
        return
    if _cs(B)!=0:
        print "B is not sorted.  Please use a pyglSort."
        return
    return _subtr2d.subtract2D(A,B,{},"")


# In[46]:

def subtract1D(PGL,BED):
    """Takes a PyGL object and a PyGL-bed object and returns a PyGL object resulting from the subtract1D operation"""
    if _cs(PGL)!=0:
        print "The PyGL supplied is not sorted.  Please use a pyglSort."
        return
    return _subtr1d.subtract1D(PGL,BED,{},"")


# In[50]:

def window(PGL,window1="%#$",window2="%#$"):
    """Takes a PyGL object and returns a PyGL object resulting from the window operation"""
    args={'window1':window1,'window2':window2}
    return _wind.window(PGL,args)


