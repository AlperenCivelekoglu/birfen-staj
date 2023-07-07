#!/usr/bin/env python

import rospy
import time
import math
import numpy as np
from geometry_msgs.msg import Twist

lx = 0.0
ly = 0.0
lz = 0.0
ax = 0.0
ay = 0.0
az = 0.0

def cmdvel_call_back(pose_messages):
    global lx, ax, ly, ay, lz, az

    lx = pose_messages.linear.x
    ly = pose_messages.linear.y
    lz = pose_messages.linear.z

    ax = pose_messages.angular.x
    ay = pose_messages.angular.y
    az = pose_messages.angular.z


def move(velocity_publisher, x, y, z):
    velocity_message = Twist()
    global lx, ax, ly
    lx0=lx
    ly0=ly
    lz0=lz

    rospy.loginfo("---------values:\nx: {} y:{} z:{}".format(lx0,ly0,lz0))
    try:
        velocity_message.linear.x = np.float64(x)
        velocity_message.linear.y = np.float64(y)
        velocity_message.linear.z = np.float64(z)
        rospy.loginfo("---------updated values:\nx: {} y:{} z:{}".format(np.float64(x),np.float64(y),np.float64(z)))
    except ValueError:
        rospy.loginfo("!!!!wrong type of input value!!!!")
        velocity_message.linear.x = lx0
        velocity_message.linear.y = ly0
        velocity_message.linear.z = lz0

    velocity_publisher.publish(velocity_message)
    

def rotate(velocity_publisher, x, y, z):
    velocity_message = Twist()
    global ay, lz, az
    ax0=ax
    ay0=ay
    az0=az

    rospy.loginfo("---------values:\nx: {} y:{} z:{}".format(ax0,ay0,az0))
    try:
        velocity_message.angular.x = np.float64(x)
        velocity_message.angular.y = np.float64(y)
        velocity_message.angular.z = np.float64(z)
        rospy.loginfo("---------updated values:\nx: {} y:{} z:{}".format(np.float64(x),np.float64(y),np.float64(z)))
    except ValueError:
        rospy.loginfo("wrong type of input value")
        velocity_message.angular.x = ax0
        velocity_message.angular.y = ay0
        velocity_message.angular.z = az0

    velocity_publisher.publish(velocity_message)

if __name__=="__main__":
    try:
        rospy.init_node("cmdvel_Publisher")

        cmdvel_topic = ("/cmd_vel")
        cmdvel_publisher = rospy.Publisher(cmdvel_topic,Twist,queue_size=10)
        
        cmdvel_topic = ("/cmd_vel")
        cmdvel_subscriber = rospy.Subscriber(cmdvel_topic,Twist,cmdvel_call_back)

        time.sleep(5)

        #move(cmdvel_publisher, -1, 0, 0)
        rotate(cmdvel_publisher, 0.6, 0, 0)
    except rospy.ROSInterruptException:
        print("Interrupted")