#README

The following steps have been followed to setup the testing environment consisting of Master-Slave Beowulf Cluster consisting
of:

1. A PC Running Kali Linux 2.0 with Intel Core i3 processor (consisting of 2 physical cores) and 6 Gigabytes of RAM.
   This PC runs the Master process and several Slave Processes(as required).
   
2. A PC Running Ubuntu 14.04 with Intel Core i5 processor (consisting of 2 physical cores) and 4 Gigabytes of RAM.
   This PC runs the Slave Processes only (number of processes vary according to the requirement).
   
3. A PC Running Ubuntu 14.04 with Intel Core i7 processor (consisting of 4 physical cores) and 8 Gigabytes of RAM.
   This PC runs the Slave Processes only (number of processes vary according to the requirement).
   
All the Machines are assumed to have Python 2.7 installed on the system.

####STEP 1: SETTING UP THE BEOWULF CLUSTER AND RUNNING A TEST PROGRAM

Follow the instructions given in the following links and test the mentioned C program.
######Setting up NFS:

  https://help.ubuntu.com/14.04/serverguide/network-file-system.html

######Setting up cluster:

  http://techtinkering.com/2009/12/02/setting-up-a-beowulf-cluster-using-open-mpi-on-linux/
  


####STEP 2: SETTING  UP PYTHON LIBRARY FOR MPI COMMUNICATION

Python library mpi4py is used in the project. Follow the installation instructions mentioned in the link below:

  http://mpi4py.readthedocs.org/en/stable/install.html
  
Run the following code to test if the module is working:
```
  from mpi4py import MPI

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()

  if rank == 0:
      data = {'a': 7, 'b': 3.14}
      comm.send(data, dest=1, tag=11)
  elif rank == 1:
      data = comm.recv(source=0, tag=11)
```  


####STEP 3: INSTALLING THE CPLEX ENGINE

Download and install the IBM's CPLEX Optimizer.
To install the CPLEX-Python modules on your system, use the script setup.py located in yourCplexhome/python/VERSION/PLATFORM. If you want to install the CPLEX-Python modules in a nondefault location, use the option --home to identify the installation directory. For example, to install in the directory yourPythonPackageshome/cplex, use the following command from the command line:
```
  python setup.py install --home yourPythonPackageshome/cplex
```


####STEP 4: RUNNING THE PROGRAM ON THE CLUSTER

Copy all the Python files to the directory of your choice (in the NFS).
Run the program with the following command:
```
  mpirun -np 7 --hostfile <hostfile name> python test2.py
```

The program will run for Random test cases and will display the output (Cluster Head nodes and Objective value).
