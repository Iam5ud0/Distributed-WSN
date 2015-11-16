#!/usr/bin/env python
# -*- coding: utf-8 -*-
#completed
from __future__ import print_function
from itertools import *
import cplex
from cplex.exceptions import CplexError
import sys
import mr,rp1,rp2,rp3
def SubC(C,prob_type):
	if prob_type=='rp1':
		for n in C:
			rp1.rows_global.append([["z_c_"+str(n.j_index)],[1]])
			rp1.sense_global+='E'
			rp1.rhs_global.append(1)
		return rp1.rp1()
	elif prob_type=='rp2':
		for n in C:
			rp2.rows_global.append([["z_c_"+str(n.j_index)],[1]])
			rp2.sense_global+='E'
			rp2.rhs_global.append(1)
		return rp2.rp2()
	elif prob_type=='rp3':
		for n in C:
			rp3.rows_global.append([["z_c_"+str(n.j_index)],[1]])
			rp3.sense_global+='E'
			rp3.rhs_global.append(1)
		return rp3.rp3()
	elif prob_type=='mr':
		for n in C:
			mr.rows_global.append([["z_c_"+str(n.j_index)],[1]])
			mr.sense_global+='E'
			mr.rhs_global.append(1)
		return mr.mr()
	else:
		sys.exit(0)

