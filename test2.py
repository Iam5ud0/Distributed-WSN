import random
from node import *
from m1m3 import *
from SearchSubC import *
from SearchSubS import *
import mr,rp1,rp2,rp3,p
import cplex
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank=comm.Get_rank()
print ":::::::+++++++:::::::",rank
I,J,K=[],[],[]

def distance(i,j):#finds distance b/w nodes with index i and j
	return math.sqrt((I[i].x-I[j].x)**2+(I[i].y-I[j].y)**2)

def fillDistances():
	global Dist
	for i in xrange(len(I)):
		for j in xrange(len(I)):
			Dist[i][j]=distance(i,j)

N=50
C=3
S=2
U=S
H=C

#-----------PROCESS 1---MASTER--------BEGIN------------------------

if rank == 0:
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
	S_b_mr,Z_Sb_mr=ConstructM1M3(I,J,K,Dist,N,H,prob_type)

	prob_type2="rp1"
	S_b_rp1, Z_Sb_rp1 = ConstructM1M3(I,J,K,Dist,N,H,prob_type2)

	prob_type3="rp2"
	S_b_rp2, Z_Sb_rp2 = ConstructM1M3(I,J,K,Dist,N,H,prob_type3)

	prob_type4="rp3"
	S_b_rp3, Z_Sb_rp3 = ConstructM1M3(I,J,K,Dist,N,H,prob_type4)

	prob_type5="p"
	S_b_p, Z_Sb_p = ConstructM1M3(I,J,K,Dist,N,H,prob_type5)

	comm.send(I,dest=1,tag=1)
	comm.send(J,dest=1,tag=2)
	comm.send(K,dest=1,tag=6)
	comm.send(Dist,dest=1,tag=3)
	comm.send(N,dest=1,tag=4)
	comm.send(H,dest=1,tag=5)
	comm.send(S_b_mr,dest=1,tag=20)
	comm.send(Z_Sb_mr,dest=1,tag=30)
	comm.send(prob_type,dest=1,tag=8)

	comm.send(I,dest=2,tag=1)
	comm.send(J,dest=2,tag=2)
	comm.send(K,dest=2,tag=6)
	comm.send(Dist,dest=2,tag=3)
	comm.send(N,dest=2,tag=4)
	comm.send(H,dest=2,tag=5)
	comm.send(S_b_rp2,dest=2,tag=22)
	comm.send(Z_Sb_rp2,dest=2,tag=32)
	comm.send(prob_type3,dest=2,tag=8)

	comm.send(I,dest=3,tag=1)
	comm.send(J,dest=3,tag=2)
	comm.send(K,dest=3,tag=6)
	comm.send(Dist,dest=3,tag=3)
	comm.send(N,dest=3,tag=4)
	comm.send(H,dest=3,tag=5)
	comm.send(S_b_rp3,dest=3,tag=23)
	comm.send(Z_Sb_rp3,dest=3,tag=33)
	comm.send(prob_type4,dest=3,tag=8)

	#send initial solutions to 4 through p
	comm.send(I,dest=4,tag=1)
	comm.send(J,dest=4,tag=2)
	comm.send(K,dest=4,tag=6)
	comm.send(Dist,dest=4,tag=3)
	comm.send(N,dest=4,tag=4)
	comm.send(H,dest=4,tag=5)
	comm.send(S_b_p,dest=4,tag=24)
	comm.send(Z_Sb_p,dest=4,tag=34)
	comm.send(prob_type5,dest=4,tag=8)

	comm.send(I,dest=5,tag=1)
	comm.send(J,dest=5,tag=2)
	comm.send(K,dest=5,tag=6)
	comm.send(Dist,dest=5,tag=3)
	comm.send(N,dest=5,tag=4)
	comm.send(H,dest=5,tag=5)
	comm.send(S_b_p,dest=5,tag=24)
	comm.send(Z_Sb_p,dest=5,tag=34)
	comm.send(prob_type5,dest=5,tag=8)

	comm.send(I,dest=6, tag=1)
	comm.send(J,dest=6,tag=2)
	comm.send(K,dest=6,tag=6)
	comm.send(Dist,dest=6,tag=3)
	comm.send(N,dest=6,tag=4)
	comm.send(H,dest=6,tag=5)
	comm.send(S_b_p,dest=6,tag=24)
	comm.send(Z_Sb_p,dest=6,tag=34)
	comm.send(prob_type5,dest=6,tag=8)


	print(":::::: all initial solutions sent ::::::::")
	S_b_rp1,Z_Sb_rp1=SearchSubC(I,J,K,Dist,N,H,S_b_rp1,Z_Sb_rp1,prob_type2)
	rp1.rows_global.append([["e_c_" + str(j) for j in xrange(J_size)] + ["e_" + str(i) for i in xrange(I_size)],[1 for j in xrange(J_size)] + [1 for i in xrange(I_size)]])
	rp1.sense_global += "L"
	rp1.rhs_global.append(Z_Sb_rp1)
	Z_Sb_rp1 = rp1.rp1(I,J,K,Dist)
	print("sending Z_Sb_rp1 & 2...........")
	comm.send(Z_Sb_rp1,dest=2,tag=11)
	comm.send(Z_Sb_rp1,dest=3,tag=11)
	Z_1_LR = Z_Sb_rp1

	print("sent Z_Sb_rp1 & 2...........")

	print("receive cut 26 from proc 2")
	Z_2_LR = comm.recv(source = 2, tag =60 )

	print("receive cut 27 from proc 3")
	Z_3_UR = comm.recv(source = 3, tag =60 )

	print("receive set C from 4-p ")
	# S_best1= comm.recv(source = 4, tag = )
	# S_best2= comm.recv(source = 5, tag = )
	# S_best3= comm.recv(source = 6, tag = )
	Z_best1 = comm.recv(source = 4, tag =62 )
	Z_best2 = comm.recv(source = 5, tag =62 )
	Z_best3 = comm.recv(source = 6, tag =62 )

	print("Z_best received")

	# th4=(S_best1,Z_best1)
	# th5=(S_best2,Z_best2)
	# th6=(S_best3,Z_best3)

	Z_best = min(Z_best1, Z_best2, Z_best3)

	print("send cuts 23-27 to processes 4 through p")
	comm.send(Z_best, dest = 4, tag = 63)
	comm.send(Z_2_LR, dest = 4, tag = 64)
	comm.send(Z_1_LR, dest = 4, tag = 65)
	comm.send(Z_3_UR, dest = 4, tag = 66)

	comm.send(Z_best, dest = 5, tag = 63)
	comm.send(Z_2_LR, dest = 5, tag = 64)
	comm.send(Z_1_LR, dest = 5, tag = 65)
	comm.send(Z_3_UR, dest = 5, tag = 66)

	comm.send(Z_best, dest = 6, tag = 63)
	comm.send(Z_2_LR, dest = 6, tag = 64)
	comm.send(Z_1_LR, dest = 6, tag = 65)
	comm.send(Z_3_UR, dest = 6, tag = 66)


	#S_best = i for i in [th4,th5,th6] if min([th4[1],th5[1],th6[1]])==i[1]

	print("##################receive final sols from proc 0 ################")
	Z_proc_0=comm.recv(source=1,tag= 70)

	##################receive final sols from proc 4-p ################
	Z_proc_4=comm.recv(source=4,tag= 70)
	Z_proc_5=comm.recv(source=5,tag=70)
	Z_proc_6=comm.recv(source=6,tag= 70)

	print("lol here wait!!")

	mn=min([Z_proc_4,Z_proc_5,Z_proc_6,Z_proc_0])

	if mn==Z_proc_0:
		comm.send(1,dest=1,tag= 72)
		comm.send(0,dest=4,tag=73)
		comm.send(0,dest=5,tag=73)
		comm.send(0,dest=6,tag=73)
	elif mn==Z_proc_4:
		comm.send(0,dest=1,tag=72)
		comm.send(1,dest=4,tag=73)
		comm.send(0,dest=5,tag=73)
		comm.send(0,dest=6,tag=73)
	elif mn==Z_proc_5:
		comm.send(0,dest=1,tag=72)
		comm.send(0,dest=4,tag=73)
		comm.send(1,dest=5,tag=73)
		comm.send(0,dest=6,tag=73)
	elif mn==Z_proc_6:
		comm.send(0,dest=1,tag=72)
		comm.send(0,dest=4,tag=73)
		comm.send(0,dest=5,tag=73)
		comm.send(1,dest=6,tag=73)
	print("\n\n\n\n\n\n chk sent\n\n\n\n")





#-----------PROCESS 1-----------END------------------------





#-----------PROCESS 0-----------START--------------------
elif rank == 1:
	I=comm.recv(source=0,tag=1)
	J=comm.recv(source=0,tag=2)
	K=comm.recv(source=0,tag=6)
	Dist=comm.recv(source=0,tag=3)
	N=comm.recv(source=0,tag=4)
	H=comm.recv(source=0,tag=5)
	S_b_mr=comm.recv(source=0,tag=20)
	Z_Sb_mr=comm.recv(source=0,tag=30)
	prob_type=comm.recv(source=0,tag=8)

	print("recieved initial solutions")

	S_b_mr,Z_Sb_mr=SearchSubC(I,J,K,Dist,N,H,S_b_mr,Z_Sb_mr,prob_type)
	Z_best, Z_1_LR, Z_2_LR, Z_3_UR=0,0,0,0
	S_b_mr,Z_Sb=SearchSubS(I,J,K,Dist,N,H,U,S_b_mr,Z_Sb_mr,prob_type, Z_best, Z_1_LR, Z_2_LR, Z_3_UR)
	mr.rows_global.append([["e_c_"+str(j) for j in xrange(J_size)]+["e_"+str(i) for i in xrange(I_size)]+["E_R_max","E_R_min"],[mr.t/(I_size-J_size) for j in xrange(J_size)]+[mr.t/(I_size-J_size) for i in xrange(I_size)]+[1,-1]])
	mr.rows_global.append([["E_R_max"],[1]])
	mr.sense_global+='LG'
	mr.rhs_global.append(Z_Sb_mr)
	mr.rhs_global.append(((sum(I[i].E for i in xrange(I_size)))/(I_size))-(Z_Sb_mr/mr.t))
	Z_Sb_mr = mr.mr(I,J,K,Dist)

	print("Sending Z_Sb_mr to Master.......")

	comm.send(Z_Sb_mr, dest = 0, tag = 70)
	print("Z_Sb_mr sent! receiving chk......")

	chk=comm.recv(source=0,tag = 72)

	print("chk received")
	if chk == 1:
		mr.print_solution()
		print("end")
		sys.exit(0)
	else:
		sys.exit(0)
	# send final solution to the master

#-----------PROCESS 0-----------END------------------------


#-----------PROCESS 1----------START-----------------------
#if rank==0:
	# S_b_rp1,Z_Sb_rp1=SearchSubC(I,J,Dist,N,H,S_b_rp1,Z_Sb_rp1,prob_type2)
	# rp1.rows_global.append([["e_c_" + str(j) for j in xrange(J_size)] + ["e_" + str(i) for i in xrange(I_size)],[1 for j in xrange(J_size)] + [1 for i in xrange(I_size)]])
	# rp1.sense_global += "L"
	# rp1.rhs_global.append(Z_Sb_rp1)
	# Z_Sb_rp1 = rp1.rp1()
	# comm.send(Z_Sb_rp1,dest=2,tag=11)
	# comm.send(Z_Sb_rp1,dest=3,tag=11)


#-----------PROCESS 1-----------END------------------------



#-----------PROCESS 2----------START-----------------------
elif rank == 2:
	I=comm.recv(source=0,tag=1)
	J=comm.recv(source=0,tag=2)
	K = comm.recv(source=0, tag=6)
	Dist=comm.recv(source=0,tag=3)
	N=comm.recv(source=0,tag=4)
	H=comm.recv(source=0,tag=5)
	S_b_rp2=comm.recv(source=0,tag=22)
	Z_Sb_rp2=comm.recv(source=0,tag=32)
	prob_type3=comm.recv(source=0,tag=8)
	
	S_b_rp2,Z_Sb_rp2=SearchSubC(I,J,K,Dist,N,H,S_b_rp2,Z_Sb_rp2,prob_type3)

	print("receiving...... Z_Sb_rp1")	

	Z_Sb_rp1 = comm.recv(source = 0, tag = 11)

	print("received!!!! Z_Sb_rp1")

	rp2.rows_global.append([["E_R_max"],[1]])
	rp2.sense_global += "L"
	rp2.rhs_global.append(Z_Sb_rp2)

	rp2.rows_global.append([["e_c_" + str(j) for j in xrange(J_size)] + ["e_" + str(i) for i in xrange(I_size)],[1 for j in xrange(J_size)] + [1 for i in xrange(I_size)]])
	rp2.sense_global += "G"
	rp2.rhs_global.append(Z_Sb_rp1)

	Z_2_LR = rp2.rp2(I,J,K,Dist)

	print("submit final solutions to mastar (cut 26)")
	comm.send(Z_2_LR, dest = 0, tag = 60)
#-----------PROCESS 2-----------END------------------------




#-----------PROCESS 3----------START-----------------------
elif rank == 3:
	print("receiving init")
	I=comm.recv(source=0,tag=1)
	J=comm.recv(source=0,tag=2)
	K = comm.recv(source=0, tag=6)
	Dist=comm.recv(source=0,tag=3)
	N=comm.recv(source=0,tag=4)
	H=comm.recv(source=0,tag=5)
	S_b_rp3=comm.recv(source=0,tag=23)
	Z_Sb_rp3=comm.recv(source=0,tag=33)
	prob_type4=comm.recv(source=0,tag=8)
	print("received init")
	S_b_rp3,Z_Sb_rp3=SearchSubC(I,J,K,Dist,N,H,S_b_rp3,Z_Sb_rp3,prob_type4)

	Z_Sb_rp1 = comm.recv(source = 0, tag = 11)

	rp3.rows_global.append([["E_R_min"],[1]])
	rp3.sense_global += "G"
	rp3.rhs_global.append(Z_Sb_rp3)

	rp3.rows_global.append([["e_c_" + str(j) for j in xrange(J_size)] + ["e_" + str(i) for i in xrange(I_size)],[1 for j in xrange(J_size)] + [1 for i in xrange(I_size)]])
	rp3.sense_global += "G"
	rp3.rhs_global.append(Z_Sb_rp1)

	Z_3_UR = rp3.rp3(I,J,K,Dist)

	print ("submit final solutions to mastar (cut 27)")
	comm.send(Z_3_UR, dest = 0, tag = 60)
#-----------PROCESS 3-----------END------------------------





#-----------PROCESS 4 through p----------START-----------------------
elif rank > 3:
	I = comm.recv(source=0,tag=1)
	J = comm.recv(source=0,tag=2)
	K = comm.recv(source=0,tag=6)
	Dist = comm.recv(source=0,tag=3)
	N = comm.recv(source=0,tag=4)
	H = comm.recv(source=0,tag=5)
	S_b_p = comm.recv(source=0,tag =24)
	Z_Sb_p = comm.recv(source=0,tag =34)
	prob_type5 = comm.recv(source=0,tag =8)
	
	S_b_p,Z_Sb_p = SearchSubC(I,J,K,Dist,N,H,S_b_p,Z_Sb_p,prob_type5)

	# comm.send(S_b_p,dest=0,tag=)
	print("send S_b_p,Z_Sb_p to master")
	comm.send(Z_Sb_p,dest=0,tag=62)
	

	print("get back cuts 23-27")
	Z_best = comm.recv(source = 0, tag = 63)
	Z_1_LR = comm.recv(source = 0, tag = 64)
	Z_2_LR = comm.recv(source = 0, tag = 65)
	Z_3_UR = comm.recv(source = 0, tag = 66)

	print("perform SearchSubS with these cuts")

	S_b_p,Z_Sb_p = SearchSubS(I,J,K,Dist,N,H,U,S_b_p,Z_Sb_p,prob_type5, Z_best, Z_1_LR, Z_2_LR, Z_3_UR)

	print("send final solutions to master")
	comm.send(Z_Sb_p, dest = 0, tag = 70)
	print("receiving chk")
	chk=comm.recv(source=0,tag = 73)
	if chk == 1:
		print(S_b_p,Z_Sb_p)
		print("end")
		sys.exit(0)
	else:
		sys.exit(0)
#-----------PROCESS 4 through p-----------END------------------------
else : 
	print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n :::::::+++++++:::::::",rank