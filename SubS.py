#!/usr/bin/env python
# -*- coding: utf-8 -*-
#completed
from __future__ import print_function
from itertools import *
import cplex
from cplex.exceptions import CplexError
import sys
import mr,rp1,rp2,rp3, p
from node import *
def SubS(I,J,K,Dist,C,prob_type, Z_best, Z_1_LR, Z_2_LR, Z_3_UR):
	if prob_type=='rp1':
		for n in C:
			rp1.rows_global.append([["z_u_"+str(n.k_index)],[1]])
			rp1.sense_global+='E'
			rp1.rhs_global.append(1)
		return rp1.rp1(I,J,K,Dist)
	elif prob_type=='rp2':
		for n in C:
			rp2.rows_global.append([["z_u_"+str(n.k_index)],[1]])
			rp2.sense_global+='E'
			rp2.rhs_global.append(1)
		return rp2.rp2(I,J,K,Dist)
	elif prob_type=='rp3':
		for n in C:
			rp3.rows_global.append([["z_u_"+str(n.k_index)],[1]])
			rp3.sense_global+='E'
			rp3.rhs_global.append(1)
		return rp3.rp3(I,J,K,Dist)
	elif prob_type=='mr':
		for n in C:
			mr.rows_global.append([["z_u_"+str(n.k_index)],[1]])
			mr.sense_global+='E'
			mr.rhs_global.append(1)
		return mr.mr(I,J,K,Dist)
	elif prob_type=='p':
		p.rows_global.append([["e_c_"+str(j) for j in xrange(J_size)]+["e_"+str(i) for i in xrange(I_size)]+["E_R_max","E_R_min"],[mr.t/(I_size-J_size) for j in xrange(J_size)]+[mr.t/(I_size-J_size) for i in xrange(I_size)]+[1,-1]])
		p.sense_global += "L"
		p.rhs_global.append(Z_best)

		p.rows_global.append([["E_R_max"],[1]])
		p.sense_global += "G"
		p.rhs_global.append(((sum(I[i].E for i in xrange(I_size)))/(I_size))-(Z_best/p.t))

		p.rows_global.append([["e_c_" + str(j) for j in xrange(J_size)] + ["e_" + str(i) for i in xrange(I_size)],[1 for j in xrange(J_size)] + [1 for i in xrange(I_size)]])
		p.sense_global += "G"
		p.rhs_global.append(Z_1_LR)

		p.rows_global.append([["E_R_max"], [1]])
		p.sense_global += "G"
		p.rhs_global.append(Z_2_LR)

		p.rows_global.append([["E_R_min"], [1]])
		p.sense_global += "L"
		p.rhs_global.append(Z_3_UR)

		return p.p(I,J,K,Dist)
	else:
		sys.exit(0)

