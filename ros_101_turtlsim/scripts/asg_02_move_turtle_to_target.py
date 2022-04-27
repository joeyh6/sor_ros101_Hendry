#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time
import math
from math import pi


x_current = 0
y_current = 0
theta_current = 0
#x_target = 0
#y_target = 0
threshold_linear = 0.5
threshold_angular = 0.05
speed_scale_factor = 0.2

def get_distance_to_target():
	x_diagonal= x_target - x_current
	y_diagonal= y_target - y_current
	distance = math.sqrt((x_diagonal*x_diagonal)+(y_diagonal*y_diagonal))
	print(f"Distance_to_target: {distance:.2f}")
	return distance
	
def is_far_from_target(threshold, get_distance_to_target):
	return (get_distance_to_target > threshold)

def get_delta_angle_to_target():
	theta_target = math.atan2((y_target-y_current) , (x_target-x_current))
#	print(f"theta_target: {theta_target:.2f}")	 
	return (theta_target-theta_current)
	
def is_pointing_to_target(threshold, get_delta_angle_to_target):
	print(f"Delta_angle_to_target: {get_delta_angle_to_target:.2f}")
	return (get_delta_angle_to_target < threshold)

def pose_callback(data):
	global x_current
	global y_current
	global theta_current
	x_current = data.x
	y_current = data.y
	theta_current = data.theta
	
def angular_velocity_command(get_delta_angle_to_target):
	start_time = time.time()
	if (time.time()- start_time) < 1:
		msg.linear.x = 0.0
		msg.angular.z = speed_scale_factor*get_delta_angle_to_target
		publisher.publish(msg)
		time.sleep(0.1)
	msg.angular.z = 0.0
	publisher.publish(msg) 

def linear_velocity_command(get_distance_to_target):
	start_time = time.time()
	if (time.time()- start_time) < 1:
		msg.linear.x = max(get_distance_to_target*speed_scale_factor,0.1)
		msg.angular.z = 0.0
		publisher.publish(msg)
		time.sleep(0.2)
	msg.linear.x = 0.0
	publisher.publish(msg)

	
rospy.init_node("move_turtle_to_target")
rospy.Subscriber("/turtle1/pose", Pose, pose_callback)

x_target = float(input("Enter Target X Coordinate: "))
y_target = float(input("Enter Target Y Coordinate: "))


publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10);
gap_pub = rospy.Publisher("/gap", Float64, queue_size=10);
msg = Twist()

# Turn to the target direction
while not (is_pointing_to_target(threshold_angular, abs(get_delta_angle_to_target()))):	
	angular_velocity_command(get_delta_angle_to_target())
		
while (is_far_from_target(threshold_linear, get_distance_to_target())):
	linear_velocity_command(get_distance_to_target())
		
