#!/usr/bin/env python
# -*- coding: utf-8 -*-
#completed
from __future__ import print_function
from itertools import *
import cplex
from cplex.exceptions import CplexError
import sys
from node import *

w,v,c,r=50,100,50,30
s=0.3
C,S=3,2
T,t=4000,5

obj_global=[]
colnames_global=[]
lb_global=[]
ub_global=[]
ctype_global=[]
rows_global=[]
sense_global=''
rhs_global=[]

def p(I,J,K,Dist):
	obj=[0 for i in xrange(len(J)) for i in xrange(len(J))] \
		+[0 for i in xrange(len(J)) for i in xrange(len(K))] \
		+[0 for i in xrange(len(I)) for i in xrange(len(J))] \
		+[0 for j in xrange(len(I))] \
		+[0 for i in xrange(len(K))] \
		+[(t/len(I)) for i in xrange(len(I))] \
		+[(t/len(I)) for i in xrange(len(J))] \
		+[1] \
		+[-1]#[1 for i in xrange(len(I))]
		
	colnames=["x_cc_"+str(i)+"_"+str(j) for i in xrange(len(J))  for j in xrange(len(J))] \
		+["x_u_"+str(i)+"_"+str(j) for i in xrange(len(J)) for j in xrange(len(K))] \
		+["x_c_"+str(i)+"_"+str(j) for i in xrange(len(I)) for j in xrange(len(J))] \
		+["z_c_"+str(j) for j in xrange(len(I))] \
		+["z_u_"+str(i) for i in xrange(len(K))] \
		+["e_"+str(i) for i in xrange(len(I))] \
		+["e_c_"+str(i) for i in xrange(len(J))] \
		+["E_R_max","E_R_min"] 
	
	lb = [0 for i in xrange(len(J)) for i in xrange(len(J))] \
		+[0 for i in xrange(len(J)) for i in xrange(len(K))] \
		+[0 for i in xrange(len(I)) for i in xrange(len(J))] \
		+[0 for j in xrange(len(I))] \
		+[0 for i in xrange(len(K))] \
		+[0 for i in xrange(len(I))] \
		+[0 for i in xrange(len(J))] \
		+[0] \
		+[0] 
		
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


	rows = \
		[[['x_u_'+str(m)+"_"+str(k) for k in xrange(len(K))]+['x_cc_'+str(m)+"_"+str(jay) for jay in xrange(len(J)) if jay!=m]+['x_cc_'+str(jay)+"_"+str(m) for jay in xrange(len(J))  if jay!=m]+['x_c_'+str(i)+"_"+str(m) for i in xrange(len(I))]+['e_c_'+str(m)],\
		[T*(w+v*(Dist[I[J[m].index].index][I[K[k].index].index]**2)) for k in xrange(len(K))]+[T*(w+v*(Dist[I[J[m].index].index][I[J[jay].index].index]**2)) for jay in xrange(len(J))  if jay!=m]+[T*w  for jay in xrange(len(J))  if jay!=m]+[T*(w+c*s)*I[i].R for i in xrange(len(I))]+[-1]] for m in xrange(len(J))]+\
		[[['x_c_'+str(i)+"_"+str(j) for j in xrange(len(J))]+["e_"+str(i)],\
		[(T*(w+v*(Dist[i][J[j].index]**2))*I[i].R) for j in xrange(len(J))]+[-1]] for i in xrange(len(I))]+\
		[[['x_u_'+str(m)+"_"+str(k) for k in xrange(len(K))]+['x_cc_'+str(m)+"_"+str(j) for j in xrange(len(J)) if j!=m]+['x_cc_'+str(j)+"_"+str(m) for j in xrange(len(J)) if j!=m]+['x_c_'+str(i)+"_"+str(m) for i in xrange(len(I))],\
		[1 for k in xrange(len(K))]+[1 for j in xrange(len(J)) if j!=m]+[-1  for j in xrange(len(J)) if j!=m]+[(s-1)*I[i].R for i in xrange(len(I))]] for m in xrange(len(J))]+\
		[[['x_c_'+str(i)+"_"+str(j) for j in xrange(len(J))],\
		[1 for j in xrange(len(J))]] for i in xrange(len(I))]+\
		[[['x_c_'+str(i)+"_"+str(j)]+['z_c_'+str(j)],\
		[1]+[(-1)*(r/Dist[i][J[j].index])]]for i in xrange(len(I)) for j in xrange(len(J)) if i!=J[j].index]+\
		[[['x_cc_'+str(m)+"_"+str(j)]+['z_c_'+str(j)],\
		[1]+[(-1)*(r/Dist[J[m].index][J[j].index])*(sum(i.R for i in I))]]for m in xrange(len(J)) for j in xrange(len(J)) if m!=j]+\
		[[['x_u_'+str(j)+"_"+str(k)]+['z_u_'+str(k)],\
		[1]+[(-1)*(r/Dist[J[j].index][K[k].index])*(sum(i.R for i in I))]]for j in xrange(len(J)) for k in xrange(len(K))]+\
		[[['z_c_'+str(j) for j in xrange(len(J))],\
		[1 for j in xrange(len(J))]]]+\
		[[['z_u_'+str(k) for k in xrange(len(K))],\
		[1 for k in xrange(len(K))]]]+\
		[[['e_'+str(i)],\
		[1]] for i  in xrange(len(I))]+\
		[[['z_c_'+str(j)]+['e_c_'+str(j)]+['E_R_max'],\
		[J[j].E]+[-1]+[-1]]for j in xrange(len(J))]+\
		[[['z_c_'+str(i)]+['e_'+str(i)]+['E_R_max'],\
		[(-1)*I[i].E]+[-1]+[-1]]for i in xrange(len(I))]+\
		[[['e_'+str(i)]+['E_R_min'],\
		[1]+[1]] for i in xrange(len(I))]


	sense= 'E'*len(J)+'E'*len(I)+'E'*len(J)+'L'*len(I)+'L'*((len(I)*len(J)) - len(J))+'L'*(len(J)**2 - len(J))+'L'*(len(K)*len(J))+'EE'+'L'*len(I)+'L'*len(J)+'L'*len(I)+'L'*len(I)

	rhs=[0]*len(J)+[0]*len(I)+[0]*len(J)+[1]*len(I)+[0]*((len(I)*len(J)) - len(J))+[0]*(len(J)**2 - len(J))+[0]*(len(K)*len(J))+[C]+[S]+[I[i].E for i in xrange(len(I))]+[0]*len(J)+[(-1)*I[i].E for i in xrange(len(I))]+[I[i].E for i in xrange(len(I))]
	global rows_global,sense_global,rhs_global
	rhs+=rhs_global
	sense+=sense_global
	rows+=rows_global

	rows_global=[]
	#print(rows[376])
	sense_global=''
	rhs_global=[]
	print (len(rows),len(sense),len(rhs))
	print (len(obj),len(lb),len(ub),len(ctype))
	#print("\n:\n:\n: p \n:\n:\n:",len(I),len(J),len(k))
	try:
		prob=cplex.Cplex()
		prob.set_log_stream(None)
		prob.set_error_stream(None)
		prob.set_warning_stream(None)
		prob.set_results_stream(None)
		prob.objective.set_sense(prob.objective.sense.minimize)
		prob.variables.add(obj=obj, lb=lb, ub=ub, types=ctype,names=colnames)
		prob.linear_constraints.add(lin_expr=rows, senses=sense,rhs=rhs)
		prob.solve()
	except CplexError as exc:
	        print(exc)
	        sys.exit(0)
	#print()
	# solution.get_status() returns an integer code
	#print("Solution status = ", prob.solution.get_status(), ":", end=' ')
	# the following line #prints the corresponding string
	#print(prob.solution.status[prob.solution.get_status()])
	#print("Solution value  = ", prob.solution.get_objective_value())
	return prob.solution.get_objective_value()

if __name__ == "__main__":
	p()
