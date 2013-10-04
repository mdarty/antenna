#!/usr/bin/python
from PyNEC import *
class helix(object):
    def __init__(self, length, diameter, space):
        self.length=length
        self.radius=diameter/2
        self.space=space

    def run(self):
        self.maximum=1.0
    def run_old(self):
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
        geo.helix(self.space,self.length,self.radius,self.radius,self.radius,self.radius,.002053,100,0)
    	context.geometry_complete(1)
    	context.gn_card(1, 0, 0, 0, 0, 0, 0, 0)
    	context.ex_card(0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0)
    	context.fr_card(0, 1, 144.0e6, 1)
    	context.rp_card(0, 181, 1, 0, 5, 1, 1, -90, 90, 1.0, 1.0, 1, 0)
    	#context.rp_card(0, 181, 1, 0, 5, 1, 1, -90, 0, 1.0, 1.0, 1, 0)
    	rp = context.get_radiation_pattern(0)
    	self.maximum=numpy.amax(rp.get_gain_tot())
       	#return -maximum #Negative f to find the max instead of the min

class yagi(object):
    def __init__(self, length, width, height):
        self.length=length
        self.width=width
        self.height=height

    def run(self):
    	context=nec_context()
    	geo=context.get_geometry()
