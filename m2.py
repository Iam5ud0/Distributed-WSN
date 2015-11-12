#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Algorithm 1
from random import *
from node import *
def ConstructM2():
	Z_Sb=float("inf")
	if len(J)>100:
		Maxiter=len(J)/5
	else:
		Maxiter=len(J)/2
	while Maxiter > 0 :
		C,C_bar=[],J
		h=1
		t=randint(0,len(J)-1)
		C.append(J[t])
		C_bar.pop(t)# remove the element from Cbar which is randomly chosen
		while h < H : 
			#line 7 algo 1
			J_star=C_bar[0]
			dist_max=-1
			for element_c_bar in C_bar:
				for element_c in C:
					if Dist[element_c_bar][element_c] > dist_max:
						dist_max= Dist[element_c_bar][element_c]
						J_star=element_c_bar
			#end line 7
			C.append(J_star)
			C_bar.remove(J_star)
			h+=1
		S_c=C
		#solve SubC here get Z(S_c)
		if Z_Sc < Z_Sb:
			S_b=S_c
			Z_Sb=Z_Sc
		Maxiter-=1
		
		
			
		
