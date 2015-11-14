#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Algorithm 2 - Construction Heuristic for Parallel Algorithm
from SubC import *
import random
alpha=0.8 #assume for now
def ConstructM1M3(J,Dist,N,H,prob_type):#construction heuristics for all subproblems
	F1,F2=[],[]
	Z_Sb=float("inf")
	if len(J)>100:
		Maxiter=len(J)/5
	else:
		Maxiter=len(J)/2
	Beta=(N/2)-2
	for i in J:
		if (i.x>((N-Beta)/2)+1 and i.x < ((N+Beta)/2)-1) and (i.y>((N-Beta)/2)+1 and i.y < ((N+Beta)/2)-1):
			F1.append(i)
		else:
			F2.append(i)
	print("lengths F1: F2",len(F1),len(F2))
	while Maxiter > 0 :
		C,C_bar=[],F2[:]
		h=1
		t=random.randint(0,len(F2)-1)
		C.append(F2[t])
		C_bar.pop(t)# remove the element from Cbar which is randomly chosen
		print("lengths C: C_bar",len(C),len(C_bar))
		print("lengths F1: F2",len(F1),len(F2))
		while h < H*alpha : 
			#J_star Algo 2 line 9
			lst=[]
			for element_c_bar in C_bar:
				for element_c in C:
					lst.append((Dist[element_c_bar.index][element_c.index],element_c_bar))
			lst=sorted(lst,key=lambda x : x[0])
			#line 9 end
			#print lst,h,H
			if len(lst) ==0:
				break
			J_star=lst[len(lst)/2][1]
			C.append(J_star)
			C_bar.remove(J_star)
			h+=1
			
		C_bar=F1[:]
		
		while h < H : 
			#J_star algo 2 line 15
			lst=[]
			for element_c_bar in C_bar:
				for element_c in C:
					lst.append((Dist[element_c_bar.index][element_c.index],element_c_bar))
			lst=sorted(lst,key=lambda x : x[0])
			#line 15 end
			if len(lst) ==0:
				break
			J_star=lst[len(lst)/2][1]
			C.append(J_star)
			C_bar.remove(J_star)
			h+=1
		
		S_c=C
		#solve SubC by cplex here get Z_Sc = Z(S_c)
		Z_Sc=SubC(S_c,prob_type)
		if Z_Sc < Z_Sb:
			S_b=S_c
			Z_Sb=Z_Sc
		Maxiter-=1
		return S_b,Z_Sb
		#return S_b and Z_Sb best solution and corresponding value
			
		
