#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time
import math


x_current = 0
y_current = 0
theta_current = 0
#x_target = 0
#y_target = 0


def pose_callback(data):
	global x_current
	global y_current
	global theta_current
	x_current = data.x
	y_current = data.y
	theta_current = data.theta
	
rospy.init_node("move_turtle_to_target")
rospy.Subscriber("/turtle1/pose", Pose, pose_callback)

x_target = float(input("Enter Target X Coordinate: "))
y_target = float(input("Enter Target Y Coordinate: "))

theta_target = math.atan2((y_target-y_current) , (x_target-x_current))

publisher = rospy.Publisher("/turtle1/cmd_vel", Twist, queue_size=10);
gap_pub = rospy.Publisher("/gap", Float64, queue_size=10);

msg = Twist()

# Turn to the target direction
while (abs(theta_current-theta_target) > 0.08):
#	gap = theta_target	
	start_time = time.time()
	while (time.time()- start_time) < 1:
		msg.linear.x = 0.0
		msg.angular.z = 0.1
		publisher.publish(msg)
		time.sleep(0.1)
	msg.angular.z = 0.0
	publisher.publish(msg)
		


while ((math.sqrt(((x_target - x_current)*(x_target - x_current))+((y_target - y_current)*(y_target - y_current)))) > 0.5):
	# Move forward
	start_time = time.time()
	while (time.time()- start_time) < 1:
		gap = (math.sqrt(((x_target - x_current)*(x_target - x_current))+((y_target - y_current)*(y_target - y_current))))
		gap_pub.publish(gap)
		msg.linear.x = 0.2
		msg.angular.z = 0.0
		publisher.publish(msg)
		time.sleep(0.2)
		
	msg.linear.x = 0.0
	publisher.publish(msg)
	#gap_pub.publish(gap)
		
