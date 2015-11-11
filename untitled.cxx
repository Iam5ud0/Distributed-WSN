/*
 * untitled.cxx
 * 
 * Copyright 2015 sudhakar <sudhakar@Hack-Machine>
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 * MA 02110-1301, USA.
 * 
 * 
 */


#include <iostream>
#include <bits/stdc++.h>
using namespace std;

struct node{
	float Ei; //available energy (J) at a sensor i
	float Ri; //data generation rate (bits/unit time) at a sensor i
	float x,y; //co ordinates on a 2-d plane x>0 y>0
	};

vector<struct node> F1,F2;
//vector<struct node> J;//set of candidate CHs
vector<int> J;	//set of indices corresponding to CHs


int H;		// number of cluster heads (given)

float Z(vector<struct node> ){
	//objective function for starting constructs
	
	return 0;
	}

void ContructM2(){
	//algo 1 
	int maxiter=J.size()/2 ? J.size() < 100 : J.size()/5;
		
	while (maxiter) {
		//vector<struct node> C;	// set of CH's
		vector<int> C, Cbar = J;	//  set of CH's
		
		int h = 1;
		int random = rand() % J.size();
		C.push_back(J[random]);
		Cbar.erase(Cbar.begin() + random);
		
		while (h < H) {
			jstar = 
		}	
	}
}

int main(int argc, char **argv)
{
	srand(time(NULL));
	
	return 0;
}

