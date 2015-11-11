#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from itertools import *
import cplex
from cplex.exceptions import CplexError
import sys
from node import *

I, J, K = [], [], []
w,v,c,r=50,100,50,30
s=0.3
T,t=4000,5 

obj=[0 for i in xrange(len(J)) for i in xrange(len(J))] \
	+[0 for i in xrange(len(J)) for i in xrange(len(K))] \
	+[0 for i in xrange(len(I)) for i in xrange(len(J))] \
	+[0 for i in xrange(len(I))] \
	+[0 for i in xrange(len(K))] \
	+[1 for i in xrange(len(I))] \
	+[1 for i in xrange(len(J))] \
	+[0] \
	+[0]#[1 for i in xrange(len(I))]
	
colnames=["x_cc_"+str(i[0]+str(i[1])) for i in permutations(range(len(J)),2)] \
	+["x_u_"+str(i)+str(j) for i in xrange(len(J)) for j in xrange(len(K))] \
	+["x_c_"+str(i)+str(j) for i in xrange(len(I)) for j in xrange(len(J))] \
	+["z_c_"+str(i) for i in xrange(len(I))] \
	+["z_u_"+str(i) for i in xrange(len(K))] \
	+["e_"+str(i) for i in xrange(len(I))] \
	+["e_c_"+str(i) for i in xrange(len(J))] \
	+["E_R_max"] \
	+["E_R_min"]

lb = [0 for i in xrange(len(J)) for i in xrange(len(J))] \
	+[0 for i in xrange(len(J)) for i in xrange(len(K))] \
	+[0 for i in xrange(len(I)) for i in xrange(len(J))] \
	+[0 for i in xrange(len(I))] \
	+[0 for i in xrange(len(K))] \
	+[0 for i in xrange(len(I))] \
	+[0 for i in xrange(len(J))] \
	+[0] \
	+[0] \
	
ub = [cplex.infinity for i in xrange(len(J)) for i in xrange(len(J))] \
	+[cplex.infinity for i in xrange(len(J)) for i in xrange(len(K))] \
	+[1 for i in xrange(len(I)) for i in xrange(len(J))] \
	+[1 for i in xrange(len(I))] \
	+[1 for i in xrange(len(K))] \
	+[cplex.infinity for i in xrange(len(I))] \
 	+[cplex.infinity for i in xrange(len(J))] \
	+[cplex.infinity] \
	+[cplex.infinity]

ctype = "".join(["C" for i in xrange(len(J)) for i in xrange(len(J))] \
	+["C" for i in xrange(len(J)) for i in xrange(len(K))] \
	+["I" for i in xrange(len(I)) for i in xrange(len(J))] \
	+["I" for i in xrange(len(I))] \
	+["I" for i in xrange(len(K))] \
	+["C" for i in xrange(len(I))] \
	+["C" for i in xrange(len(J))] \
	+["C"] \
	+["C"])


rows = [\
	[['x_u_'+str(m)+str(k) for k in xrange(len(K))]+['x_cc_'+str(m)+str(j) for j in filter(lambda x: x!= m,range(len(J)))]+['x_cc_'+str(j)+str(m) for j in filter(lambda x: x!= m,range(len(J)))]+['x_c_'+str(i)+str(m) for i in xrange(len(I))]+['e_c_'+str(m)],\
	[T*(w+v*(Dist[I[J[m].index]][I[K[k].index]]**2)) for k in xrange(len(K))]+[T*(w+v*(Dist[I[J[m].index]][I[J[j].index]]**2)) for j in filter(lambda x: x!= m,range(len(J)))]+[T*w  for j in filter(lambda x: x!= m,range(len(J)))]+[T*(w+c*s)*I[i].R for i in xrange(len(I))]+[-1]] for m in xrange(len(J))\
	]+[[['x_c_'+str(i)+str(j) for j in xrange(len(J))]+["e_"+str(i)],\
	[(T*(w+v*(Dist[i][J[j].index]**2))*I[i].R) for j in xrange(len(J))]+[-1]] for i in xrange(len(I))]












