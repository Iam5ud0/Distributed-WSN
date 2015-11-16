import random
from node import *
from m1m3 import *
from SearchSubC import *
from SearchSubS import *
import mr,rp1,rp2,rp3
import cplex
N=50
C=3
S=2
U=S
H=C
for i in xrange(I_size):
	X=node()
	X.index=i
	X.E=random.uniform(0.3,0.5)
	#X.E=cplex.infinity

	X.R=10
	X.x=random.randrange(0,N)
	X.y=random.randrange(0,N)
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

fillDistances()
prob_type="mr"
S_b,Z_Sb=ConstructM1M3(J,Dist,N,H,prob_type)
#print(S_b,Z_Sb)
#print ("lens",len(I),len(J))
#SearchSubC(I,J,Dist,N,H,S_b,Z_Sb,prob_type)
#SearchSubS(I,K,Dist,N,H,U,S_b,Z_Sb,prob_type)