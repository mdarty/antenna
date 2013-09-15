#!/usr/bin/python
print('importing modules')
import random
import math
import numpy
from scipy.optimize import fmin_l_bfgs_b as minimize
from PyNEC import *

#Length units in meters

random.seed()
xbounds=[(0.1,0.4),(0.1,2.0),(0.05,0.5)]

def function(x):
	context=nec_context()
	geo=context.get_geometry()
	#helix(int tag_id, int segcount, double s, double hl, double a1, double b1, double a2, dboule b2, double rad)
	           # \param tag_id The tag ID.
	           # \param segment_count The number of segments.
	           # \param s The turn spacing.
	           # \param h1 The total length of the helix (negative for a left-handed helix).
	           # \param a1 x-start radius.
	           # \param b1 y-start radius.
	           # \param a2 x-end radius.
	           # \param b2 y-end radius.
	           # \param rad The wire radius.

		#the last 2 should be insegcount, int tag_id not the first 2 had to look at c code to find this

	#geo.helix(0,segment_count,space,length_helix,radius_helix,radius_helix,radius_helix,radius_helix,.001)
	#geo.helix(.249328,1.24664,.159155,.159155,.159155,.159155,.001,100,0)
	radius=x[0]
	length=x[1]
	space=x[2]
	geo.helix(space,length,radius,radius,radius,radius,.002053,100,0)
	context.geometry_complete(1)
	context.gn_card(1, 0, 0, 0, 0, 0, 0, 0)
	context.ex_card(0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0)
	context.fr_card(0, 1, 144.0e6, 1)
	context.rp_card(0, 181, 1, 0, 5, 1, 1, -90, 90, 1.0, 1.0, 1, 0)
	#context.rp_card(0, 181, 1, 0, 5, 1, 1, -90, 0, 1.0, 1.0, 1, 0)
	rp = context.get_radiation_pattern(0)
	maximum=numpy.amax(rp.get_gain_tot())
   	return -maximum #Negative f to find the max instead of the min

#Latin hypercube
def hyp():
	rad_step=0.05
	length_step=0.1
	space_step=0.05
	rad=list(numpy.arange(0.01,0.3,rad_step))
	length=list(numpy.arange(0.1,1.9,length_step))
	space=list(numpy.arange(0.05,0.4,space_step))
	random.shuffle(rad) #Creating random blocks
	random.shuffle(length) #Creating random blocks
	random.shuffle(space) #Creating random blocks
	out=[]
	for i in range(len(rad)):
	    out.append(numpy.array([random.uniform(rad[i],rad[i]+rad_step),random.uniform(length[i],length[i]+length_step),random.uniform(space[i],space[i]+space_step)])) #Creating random points inside random blocks
	return out

def mont(rad,length,space):
	ans=[]
	N=50
	for i in range(N):
	    x=numpy.array([random.gauss(rad,math.sqrt(0.001)),random.gauss(length,math.sqrt(0.001)),random.gauss(space,math.sqrt(0.001))])
	    #ans.append(minimize(function,x,bounds=xbounds,approx_grad=True,disp=False))
	    ans.append(function(x))
	
	#my=numpy.zeros(len(ans))
	#for i in range(len(ans)):
	#    my[i]=ans[i][1]

	#return -numpy.average(my), numpy.std(my)
	return numpy.array([-numpy.average(ans), numpy.std(ans)])

def opt(hyp):
	ans=[]
	stats=[]
	min=numpy.zeros((2))
	print(hyp)
	for i in range(len(hyp)):
	    tmp=minimize(function,hyp[i],bounds=xbounds,approx_grad=True,disp=False)
	    stats.append(mont(tmp[0][0],tmp[0][1],tmp[0][2]))
	    ans.append(tmp)
	    if stats[i][1]<min[0]:
		min[0]=stats[i][1]
		min[1]=i
	best=ans[int(min[1])][1]
	rad=ans[int(min[1])][0][0]
	length=ans[int(min[1])][0][1]
	space=ans[int(min[1])][0][2]
	
	print('Avg='+str(stats[int(min[1])][0])+'\tSTD='+str(stats[int(min[1])][1])+'\tRad='+str(rad)+'\tL='+str(length)+'\tSpace='+str(space))

	return best, rad, length, space

if __name__=='__main__':
	print('Generating hyp')
	hyp_val=hyp()
	print('Running opt')
	best, rad, length, space=opt(hyp_val)
	#print('Best='+str(-best))
	#print('Rad='+str(rad)+'\tLength='+str(length)+'\tSpace='+str(space))
	#print('Running mont')
	#avg, std=mont(rad,length,space)
	#print('Average='+str(avg))
	#print('STD='+str(std))

