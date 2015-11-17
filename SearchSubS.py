#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from SubS import *
def SearchSubS(I,J,K,Dist,N,H,U,Sb_init,Z_Sb_init,prob_type, Z_best, Z_1_LR, Z_2_LR, Z_3_UR):
	
	Maxiter=len(K)/2
	Z_Sb=Z_Sb_init
	S_b=Sb_init[:]
	D = []
	D_bar = K[:]
	u = 1
	
	while Maxiter > 0:
		D = []
		D_bar = K[:]
		k=random.randint(0,len(D_bar)-1)
		D.append(K[k])
		D_bar.pop(k)# remove the element from D_bar which is randomly chosen
		
		while u < U-1:
			#line 6 algo 4
			K_star=D_bar[0]
			dist_max=-1
			for element_d_bar in D_bar:
				for element_d in D:
					if Dist[element_d_bar.index][element_d.index] > dist_max:
						dist_max= Dist[element_d_bar.index][element_d.index]
						K_star=element_d_bar
			#end line 6
			D.append(K_star)
			D_bar.remove(K_star)
			print (D,D_bar)
			u += 1
		S_c = D[:]
		# Solve SubS here using CPLEX and cut with Z_hat = Z_Sb to obtain Z_Sc
		for i in S_c:
			print(i.index)
		Z_Sc=SubS(I,J,K,Dist,S_c,prob_type, Z_best, Z_1_LR, Z_2_LR, Z_3_UR)
		#skip cuts for now
		if Z_Sc < Z_Sb:
			S_b, Z_Sb = S_c[:], Z_Sc
		Maxiter -= 1
		
	# Solve SubS with Timelimit and cut with Z_hat = Z_Sb skip
	return S_b,Z_Sb
