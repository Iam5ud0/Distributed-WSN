#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import *

def SearchSubC(Sb_init,Z_Sb_init,prob_type):# from construction heuristic
	h=1
	h_max,rho,rho_min,G_max=3,5,2,0.1*Z_Sb_init
	G_star=0
	g=[0 for i in xrange(h_max)]
	g[0]=float("inf")
	if len(J)>100:
		Maxiter=len(J)/5
	else:
		Maxiter=len(J)/2
	while h <= h_max and G_star==g[h-1]:
		for j in xrange(1,h+1):
			S_c=Sb_init
			S_c_free=S_c#later alligator
			omega=[[] for i in xrange(Maxiter+1)]
			Z_min = float('inf')
			
			for i in xrange(1,Maxiter+1):
				#some shit here hood solutions
				to_be_exchanged=sample(S_c_free,j)
				#contructing omega[i] line 7 algo 3
				temp=S_C_free
				for every_node in to_be_exchanged:
					for idx,every_distance in enumerate(Dist[evry_node.index]):
						if every_distance < rho:
							omega[i].append(I[idx])
				#line 7 algo 3 end
				#line 8, 9 algo 3 start			
					for every_change in omega[i]:
						temp.remove(every_node)
						temp.append(every_change)
						Z_c = SubC(temp, prob_type)
						if Z_c < Z_min:
							Z_min = Z_c
							S_i = temp
							Z_Si = Z_min
						temp.append(every_node)
						temp.remove(every_change)
				#line 8, 9 algo 3 end
				
				if Z_Si < Z_Sc:
					S_c=S_i
			g[j]=Z_Sb-Z_Sc
			if g[j] > 0:
				S_b=S_c
				Z_Sb=Z_Sc
		g[h]=0
		for _ in xrange(1,h):
			g[h]+=g[_]
		if g[h] > G_star:
			G_star=g[h]
		if G_star > G_max and rho >= rho_min:
			rho-=1
		h+=1
		#return S_b and Z_Sb
