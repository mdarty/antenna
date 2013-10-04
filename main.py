#!/usr/bin/python
print('importing modules')
import random
import math
import numpy
import os
import sys
from time import sleep
from argparse import ArgumentParser
from scipy.optimize import fmin_l_bfgs_b as minimize
from PyNEC import *
import multiprocessing as mp
from Queue import Empty
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from antenna import *

print 'PID:\t'+str(os.getpid())
os.nice(10)
poolsize=mp.cpu_count()+2

m1=mp.Manager()
m2=mp.Manager()
#work_queue = m1.JoinableQueue()
work_queue = m1.Queue()
done_queue = m2.Queue()
#Length units in meters

#random.seed()
#xbounds=[(0.1,0.4),(0.1,2.0),(0.05,0.5)]

def run_worker():
    while True:
        try:
            obj=work_queue.get(1,1)
            #work_queue.task_done()
            obj.run()
            done_queue.put(obj,1,1)
        except Empty:
            break

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

def main():
    l=2
    d=2
    steps=10
    length=numpy.linspace(0,l,l*steps)
    diameter=numpy.linspace(0,d,d*steps)
    count=0
    print 'Filling Queue'
    for l in length:
        for d in diameter:
            space=numpy.linspace(0,l,l*steps)
            for s in space:
                work_queue.put(helix(l,d,s),1,1)
                count+=1
                sys.stdout.write('\r'+str(count))
    size=work_queue.qsize()
    print '\nProcessing '+str(count)+' antennas'
    print 'Running '+str(poolsize)+' threads'
    threads=[]
    for t in range(poolsize):
        a=mp.Process(target=run_worker)
        a.start()
        threads.append(a)
    while not work_queue.empty():
        sleep(0.25)
        sys.stdout.write('\r'+str((size-work_queue.qsize())*100/size)+'%')
    print '\nwork queue empty'
    #work_queue.join()
    for i,t in enumerate(threads):
        t.join()
    print 'Joined threads'
    print str(100*done_queue.qsize()/size)+'% passed'
    antennas=[]
    while not done_queue.empty():
        antennas.append(done_queue.get(1,1))
    #for a in antennas:
    #    print a.maximum

    print 'Done with '+str(len(antennas))+' antennas'

	#print('Generating hyp')
	#hyp_val=hyp()
	#print('Running opt')
	#best, rad, length, space=opt(hyp_val)
	#print('Best='+str(-best))
	#print('Rad='+str(rad)+'\tLength='+str(length)+'\tSpace='+str(space))
	#print('Running mont')
	#avg, std=mont(rad,length,space)
	#print('Average='+str(avg))
	#print('STD='+str(std))
if __name__=='__main__':
	main()
