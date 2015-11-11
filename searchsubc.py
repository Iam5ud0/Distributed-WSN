#!/usr/bin/env python
# -*- coding: utf-8 -*-
Z_Sb_init,Sb_init # from construction heuristic
J
def SearchSubC():
	h=1
	h_max,rho,rho_min,G_max=3,5,2,0.1*Z_Sb_init
	G_star=0
	g=[0 for i in xrange(h_max)]
	g[0]=float("inf")
	if len(J)>100:
		Maxiter=len(J)/5
	else:
		Maxiter=len(J)/2
	while h <= h_max and G_star=g[h-1]:
		for j in xrange(1,h+1):
			S_c=Sb_init
			S_c_free=S_c#later alligator
			for i in xrange(1,Maxiter+1):
				#some shit here hood solutions
				
				#
				#
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
