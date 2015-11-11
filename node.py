#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math,sys,random
I=[]# randomly generated set of nodes
J=[]# subset Of I having candidate CHs
H=10
Dist=[[ 0 for i in xrange(len(I))]for i in xrange(len(I))]
class node:
	def __init__(self):
		self.Ei=''
		self.R=''
		self.x=''
		self.y=''
		self.index=''
		self.z_c=''#boolean to check if a  node is CH
		self.e=''
		self.e_c=''
def distance(i,j):#finds distance b/w nodes with index i and j
	return math.sqrt((I[i].x-I[j].x)**2+(I[i].y-I[j].y)**2)

def fillDistances():
	for i in xrange(len(I)):
		for j in xrange(len(I)):
			Dist[i][j]=distance(i,j)

