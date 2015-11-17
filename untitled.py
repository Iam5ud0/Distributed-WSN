#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mpi4py import MPI
from node import *
import random
comm = MPI.COMM_WORLD
rank=comm.Get_rank()
I,J,K=[],[],[]
if rank ==0:
	for i in xrange(100):
		X=node()
		X.index=i
		X.E=random.uniform(0.3,0.5)
		X.R=10
		X.x=random.randrange(0,10)
		X.y=random.randrange(0,10)
		I.append(X)
		I[i].k_index=-1
		I[i].j_index=-1
	
	for j in xrange(J_size):
		J.append(I[j*3])
		I[j*3].j_index=j
		J[j].j_index=j

	for k in xrange(K_size):
		K.append(I[1+(k*3)])
		I[1+(k*3)].k_index=k
		K[k].k_index=k

	comm.send(I,dest=1,tag=1)
	comm.send(K,dest=1,tag=2)
	comm.send(J,dest=1,tag=3)

elif rank == 1:
	I=comm.recv(source=0,tag=1)
	J=comm.recv(source=0,tag=2)
	K=comm.recv(source=0,tag=3)
	print I,J,K
