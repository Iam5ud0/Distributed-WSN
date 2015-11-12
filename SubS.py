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
			rp1.row.append([["z_u_"+str(n.k_index)],[1]])
			rp1.sense.append('E')
			rp1.rhs.append(1)
		return rp1.rp1()
	elif prob_type=='rp2':
		for n in C:
			rp2.row.append([["z_u_"+str(n.k_index)],[1]])
			rp2.sense.append('E')
			rp2.rhs.append(1)
		return rp2.rp2()
	elif prob_type=='rp3':
		for n in C:
			rp3.row.append([["z_u_"+str(n.k_index)],[1]])
			rp3.sense.append('E')
			rp3.rhs.append(1)
		return rp3.rp3()
	elif prob_type=='mr':
		for n in C:
			mr.row.append([["z_u_"+str(n.k_index)],[1]])
			mr.sense.append('E')
			mr.rhs.append(1)
		return mr.mr()
	else:
		sys.exit(0)

