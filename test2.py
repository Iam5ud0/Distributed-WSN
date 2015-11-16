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
S_b_mr,Z_Sb_mr=ConstructM1M3(J,Dist,N,H,prob_type)

prob_type2="rp1"
S_b_rp1, Z_Sb_rp1 = ConstructM1M3(J,Dist,N,H,prob_type2)

prob_type3="rp2"
S_b_rp2, Z_Sb_rp2 = ConstructM1M3(J,Dist,N,H,prob_type3)

prob_type4="rp3"
S_b_rp3, Z_Sb_rp3 = ConstructM1M3(J,Dist,N,H,prob_type4)


print "\n\n\n\n\n\n\n\n\n m1m3 ended \n\n\n\n\n\n\n"

#-----------PROCESS 0-----------START--------------------

# S_b_mr,Z_Sb_mr=SearchSubC(I,J,Dist,N,H,S_b_mr,Z_Sb_mr,prob_type)
# print "\n\n\n\n\n\n\n\n\n SearchSubC ended \n\n\n\n\n\n\n"
# S_b_mr,Z_Sb=SearchSubS(I,K,Dist,N,H,U,S_b_mr,Z_Sb_mr,prob_type)
# print "\n\n\n\n\n\n\n\n\n SearchSubS ended \n\n\n\n\n\n\n"
# mr.rows_global.append([["e_c_"+str(j) for j in xrange(J_size)]+["e_"+str(i) for i in xrange(I_size)]+["E_R_max","E_R_min"],[mr.t/(I_size-J_size) for j in xrange(J_size)]+[mr.t/(I_size-J_size) for i in xrange(I_size)]+[1,-1]])
# mr.rows_global.append([["E_R_max"],[1]])
# mr.sense_global+='LG'
# mr.rhs_global.append(Z_Sb_mr)
# mr.rhs_global.append(((sum(I[i].E for i in xrange(I_size)))/(I_size))-(Z_Sb_mr/mr.t))
# print(mr.mr())

#-----------PROCESS 0-----------END------------------------


#-----------PROCESS 1----------START-----------------------
S_b_rp1,Z_Sb_rp1=SearchSubC(I,J,Dist,N,H,S_b_rp1,Z_Sb_rp1,prob_type2)
rp1.rows_global.append([["e_c_" + str(j) for j in xrange(J_size)] + ["e_" + str(i) for i in xrange(I_size)],[1 for j in xrange(J_size)] + [1 for i in xrange(I_size)]])
rp1.sense_global += "L"
rp1.rhs_global.append(Z_Sb_rp1)
Z_Sb_rp1 = rp1.rp1()
#print(rp1.rp1())

#-----------PROCESS 1-----------END------------------------



#-----------PROCESS 2----------START-----------------------
S_b_rp2,Z_Sb_rp2=SearchSubC(I,J,Dist,N,H,S_b_rp2,Z_Sb_rp2,prob_type3)
rp2.rows_global.append([["E_R_max"],[1]])
rp2.sense_global += "L"
rp2.rhs_global.append(Z_Sb_rp2)

rp2.rows_global.append([["e_c_" + str(j) for j in xrange(J_size)] + ["e_" + str(i) for i in xrange(I_size)],[1 for j in xrange(J_size)] + [1 for i in xrange(I_size)]])
rp2.sense_global += "G"
rp2.rhs_global.append(Z_Sb_rp1)

print(rp2.rp2())
#-----------PROCESS 2-----------END------------------------


#-----------PROCESS 3----------START-----------------------
# S_b_rp3,Z_Sb_rp3=SearchSubC(I,J,Dist,N,H,S_b_rp3,Z_Sb_rp3,prob_type4)
# rp3.rows_global.append([["E_R_max"],[1]])
# rp3.sense_global += "G"
# rp3.rhs_global.append(Z_Sb_rp3)

# rp3.rows_global.append([["e_c_" + str(j) for j in xrange(J_size)] + ["e_" + str(i) for i in xrange(I_size)],[1 for j in xrange(J_size)] + [1 for i in xrange(I_size)]])
# rp3.sense_global += "G"
# rp3.rhs_global.append(Z_Sb_rp1)

# print(rp3.rp3())
#-----------PROCESS 3-----------END------------------------

