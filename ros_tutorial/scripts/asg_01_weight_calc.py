#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from ros_tutorial.msg import Cylinder

from math import pi

volume = 0
density = 0

volume_found = False
density_found = False

def volume_callback(data):
	global volume
	global volume_found
	volume = data.volume
	volume_found = True
	

def density_callback(data):
	global density
	global density_found
	density = data.data
	density_found = True
	
def calculate():
	if volume_found and density_found :
		weight = density * volume
		pub.publish(weight)
	
rospy.init_node("weight_calc")
rospy.Subscriber("/cylinder", Cylinder, volume_callback)
rospy.Subscriber("/density", Float64, density_callback)
pub = rospy.Publisher("/weight", Float64, queue_size=10);


while not rospy.is_shutdown():
	calculate()
	rospy.sleep(0.1)


