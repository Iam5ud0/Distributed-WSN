#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math,sys,random
I=[]# randomly generated set of nodes
L=[]# subset Of I having sensors
J=[]# subset Of I having candidate CHs
K=[]# subset Of I having candidate sinks
I_size=30
J_size=7
K_size=8
Dist=[[ 0 for i in xrange(I_size)]for i in xrange(I_size)]
class node:
	def __init__(self):
		self.E=''
		self.R=''
		self.x=''
		self.y=''
		self.index=''
		self.z_c=''#boolean to check if a  node is CH
		self.e=''
		self.e_c=''
		self.j_index=''
		self.k_index=''
def distance(i,j):#finds distance b/w nodes with index i and j
	return math.sqrt((I[i].x-I[j].x)**2+(I[i].y-I[j].y)**2)

def fillDistances():
	global Dist
	for i in xrange(len(I)):
		for j in xrange(len(I)):
			Dist[i][j]=distance(i,j)