#!/usr/bin/env python
# -*- coding: utf-8 -*-

S_b # initialize to best solution here

K = [] # generate them randomly
U = 8	# number of sinks

def SearchSubU(prob_type):
	
	Maxiter=len(K)/2
	
	D = []
	D_bar = K
	u = 1
	
	while Maxiter > 0:
		k=randint(0,len(D_bar)-1)
		D.append(K[k])
		D_bar.pop(k)# remove the element from D_bar which is randomly chosen
		
		while u < U:
			#line 6 algo 4
			K_star=D_bar[0]
			dist_max=-1
			for element_d_bar in D_bar:
				for element_d in D:
					if Dist[element_d_bar][element_d] > dist_max:
						dist_max= Dist[element_d_bar][element_d]
						K_star=element_d_bar
			#end line 6
			D.append(K_star)
			D_bar.remove(K_star)
			u += 1
		S_c = D
		# Solve SubS here using CPLEX and cut with Z_hat = Z_Sb to obtain Z_Sc
		Z_Sc=SubS(S_c,prob_type)
		#skip cuts for now
		if Z_Sc < Z_Sb:
			S_b, Z_Sb = S_c, Z_Sc
		Maxiter -= 1
		
	# Solve SubS with Timelimit and cut with Z_hat = Z_Sb skip
	#return S_b and Z_Sb
