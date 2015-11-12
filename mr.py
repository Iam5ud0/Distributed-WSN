#!/usr/bin/env python
# -*- coding: utf-8 -*-
#completed
from __future__ import print_function
from itertools import *
import cplex
from cplex.exceptions import CplexError
import sys
from node import *

I, J, K = [], [], []
w,v,c,r=50,100,50,30
s=0.3
C,S=0,0
T,t=4000,5 

obj=[0 for i in xrange(len(J)) for i in xrange(len(J))] \
	+[0 for i in xrange(len(J)) for i in xrange(len(K))] \
	+[0 for i in xrange(len(I)) for i in xrange(len(J))] \
	+[0 for j in xrange(len(J))] \
	+[0 for i in xrange(len(K))] \
	+[(t/len(I)) for i in xrange(len(I))] \
	+[(t/len(I)) for i in xrange(len(J))] \
	+[1] \
	+[-1]#[1 for i in xrange(len(I))]
	
colnames=["x_cc_"+str(i[0]+str(i[1])) for i in permutations(range(len(J)),2)] \
	+["x_u_"+str(i)+str(j) for i in xrange(len(J)) for j in xrange(len(K))] \
	+["x_c_"+str(i)+str(j) for i in xrange(len(I)) for j in xrange(len(J))] \
	+["z_c_"+str(j) for j in xrange(len(J))] \
	+["z_u_"+str(i) for i in xrange(len(K))] \
	+["e_"+str(i) for i in xrange(len(I))] \
	+["e_c_"+str(i) for i in xrange(len(J))] \
	+["E_R_max"] \
	+["E_R_min"]

lb = [0 for i in xrange(len(J)) for i in xrange(len(J))] \
	+[0 for i in xrange(len(J)) for i in xrange(len(K))] \
	+[0 for i in xrange(len(I)) for i in xrange(len(J))] \
	+[0 for j in xrange(len(J))] \
	+[0 for i in xrange(len(K))] \
	+[0 for i in xrange(len(I))] \
	+[0 for i in xrange(len(J))] \
	+[0] \
	+[0] \
	
ub = [cplex.infinity for i in xrange(len(J)) for i in xrange(len(J))] \
	+[cplex.infinity for i in xrange(len(J)) for i in xrange(len(K))] \
	+[cplex.infinity for i in xrange(len(I)) for i in xrange(len(J))] \
	+[1 for i in xrange(len(J))] \
	+[1 for i in xrange(len(K))] \
	+[cplex.infinity for i in xrange(len(I))] \
 	+[cplex.infinity for i in xrange(len(J))] \
	+[cplex.infinity] \
	+[cplex.infinity]

ctype = "".join(["C" for i in xrange(len(J)) for i in xrange(len(J))] \
	+["C" for i in xrange(len(J)) for i in xrange(len(K))] \
	+["I" for i in xrange(len(I)) for i in xrange(len(J))] \
	+["I" for i in xrange(len(J))] \
	+["I" for i in xrange(len(K))] \
	+["C" for i in xrange(len(I))] \
	+["C" for i in xrange(len(J))] \
	+["C"] \
	+["C"])


rows = \
	[[['x_u_'+str(m)+str(k) for k in xrange(len(K))]+['x_cc_'+str(m)+str(j) for j in filter(lambda x: x!= m,range(len(J)))]+['x_cc_'+str(j)+str(m) for j in filter(lambda x: x!= m,range(len(J)))]+['x_c_'+str(i)+str(m) for i in xrange(len(I))]+['e_c_'+str(m)],\
	[T*(w+v*(Dist[I[J[m].index]][I[K[k].index]]**2)) for k in xrange(len(K))]+[T*(w+v*(Dist[I[J[m].index]][I[J[j].index]]**2)) for j in filter(lambda x: x!= m,range(len(J)))]+[T*w  for j in filter(lambda x: x!= m,range(len(J)))]+[T*(w+c*s)*I[i].R for i in xrange(len(I))]+[-1]] for m in xrange(len(J))]+\
	[[['x_c_'+str(i)+str(j) for j in xrange(len(J))]+["e_"+str(i)],\
	[(T*(w+v*(Dist[i][J[j].index]**2))*I[i].R) for j in xrange(len(J))]+[-1]] for i in xrange(len(I))]+\
	[[['x_u_'+str(m)+str(k) for k in xrange(len(K))]+['x_cc_'+str(m)+str(j) for j in filter(lambda x: x!= m,range(len(J)))]+['x_cc_'+str(j)+str(m) for j in filter(lambda x: x!= m,range(len(J)))]+['x_c_'+str(i)+str(m) for i in xrange(len(I))],\
	[1 for k in xrange(len(K))]+[1 for j in filter(lambda x: x!= m,range(len(J)))]+[-1  for j in filter(lambda x: x!= m,range(len(J)))]+[(s-1)*I[i].R for i in xrange(len(I))]] for m in xrange(len(J))]+\
	[[['x_c_'+str(i)+str(j) for j in xrange(len(J))],\
	[1 for j in xrange(len(J))]] for i in xrange(len(I))]+\
	[[['x_c_'+str(i)+str(j)]+['z_c_'+str(j)],\
	[1]+[(-1)*(r/Dist[i][J[j].index])]]for i in xrange(len(I)) for j in xrange(len(J))]+\
	[[['x_cc_'+str(m)+str(j)]+['z_c_'+str(j)],\
	[1]+[(-1)*(r/Dist[J[m].index][J[j].index])*(sum(i.R for i in I))]]for m in xrange(len(J)) for j in xrange(len(J))]+\
	[[['x_u_'+str(j)+str(k)]+['z_u_'+str(k)],\
	[1]+[(-1)*(r/Dist[J[j].index][K[k].index])*(sum(i.R for i in I))]]for j in xrange(len(J)) for k in xrange(len(K))]+\
	[[['x_c_'+str(j)+str(k)]+['z_c_'+str(k)],\
	[1]+[(-1)*(r/Dist[J[j].index][K[k].index])*(sum(i.R for i in I))]]for j in xrange(len(J)) for k in xrange(len(K))]+\
	[['z_c_'+str(j) for j in xrange(len(J))],\
	[1 for j in xrange(len(J))]]+\
	[['z_u_'+str(k) for k in xrange(len(K))],\
	[1 for k in xrange(len(K))]]+\
	[[['e_'+str(i)],\
	[1]] for i  in xrange(len(I))]+\
	[[['e_c_'+str(j)],\
	[1]] for j in xrange(len(J))]+\
	[[['z_c_'+str(j)]+['e_c_'+str(j)]+['E_r_max'],\
	[J[j].E]+[-1]+[-1]]for j in xrange(len(J))]+\
	[[['z_'+str(i)]+['e_'+str(i)]+['E_r_max'],\
	[(-1)*I[i].E]+[-1]+[-1]]for i in xrange(len(I))]+\
	[[['e_'+str(i)]+['E_r_min'],\
	[1]+[1]] for i in xrange(len(I))]+\
	[[['e_c_'+str(j)]+['E_r_min'],\
	[1]+[1]] for j in xrange(len(J))]

sense= 'E'*len(J)+'E'*len(I)+'E'*len(J)+'E'*len(I)+'L'*(len(I)*len(J))+'L'*(len(J)**2)+'L'*(len(K)*len(J))+'L'*(len(K)*len(J))+'EE'+'L'*len(I)+'L'*len(J)+'L'*len(J)+'L'*len(I)+'L'*len(I)+'L'*len(J)

rhs=[0]*len(J)+[0]*len(I)+[0]*len(J)+[1]*len(I)+[0]*(len(I)*len(J))+[0]*(len(J)**2)+[0]*(len(K)*len(J))+[0]*(len(K)*len(J))+[C]+[S]+[I[i].E for i in xrange(len(I))]+[J[j].E for j in xrange(len(J))]+[0]*len(J)+[(-1)*I[i].E for i in xrange(len(I))]+[I[i].E for i in xrange(len(I))]+[(-1)*J[j].E for j in xrange(len(J))]
def mr():
	try:
		prob=cplex.Cplex()
		prob.objective.set_sense(prob.objective.sense.minimize)
		prob.variables.add(obj=obj, lb=lb, ub=ub, types=ctype,names=colnames)
		prob.linear_constraints.add(lin_expr=rows, senses=sense,rhs=rhs)
		prob.solve()
	except CplexError as exc:
	        print(exc)
	        sys.exit(0)
	print()
	# solution.get_status() returns an integer code
	print("Solution status = ", my_prob.solution.get_status(), ":", end=' ')
	# the following line prints the corresponding string
	print(my_prob.solution.status[my_prob.solution.get_status()])
	print("Solution value  = ", my_prob.solution.get_objective_value())

if __name__ == "__main__":
	mr()
