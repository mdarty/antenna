#!/usr/bin/python2
import sys
from PyNEC import *
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
segment_count=60
space=.249328
length_helix=1.24664
radius_helix=.001
#geo.helix(0,segment_count,space,length_helix,radius_helix,radius_helix,radius_helix,radius_helix,.001)
geo.helix(.249328,1.24664,.159155,.159155,.159155,.159155,.001,100,0)
context.geometry_complete(1)
context.gn_card(1, 0, 0, 0, 0, 0, 0, 0)
#context.ld_card(5, 0, 0, 0, 3.72e7, 0.0, 0.0)
#context.pt_card(0, 0, 1, 10)
context.ex_card(0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0)
context.fr_card(0, 1, 144.0e6, 1)
context.rp_card(0, 181, 1, 0, 5, 1, 1, -90, 90, 1.0, 1.0, 1, 0)
#context.rp_card(0, 181, 1, 0, 5, 1, 1, -90, 0, 1.0, 1.0, 1, 0)
rp = context.get_radiation_pattern(0)
print(rp.get_radial_attenuation())
print(rp.get_calculation_mode())
#print(rp.get_coordinates())
#print(rp.get_gain_type())
#print(rp.get_output_format())
#print(rp.get_gain_minor_axis())
print(rp.get_gain_tot())
print(numpy.amax(rp.get_gain_tot()))
#context.pt_card(2, 0, 5, 5)
#context.xq_card(0)
#nrp=context.get_norm_rx_pattern(0)
#print(nrp.get_coordinates())
#print(nrp.get_gain())
