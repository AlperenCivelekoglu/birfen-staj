#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math

dt = None
thr1 = 0.8
thr2 = 0.8

def callback(data):
    global dt
    dt = data
    rospy.loginfo('-------------------------------------------')
    rospy.loginfo('Range data at 0 deg:   {}'.format(dt.ranges[0]))
    rospy.loginfo('Range data at 15 deg:   {}'.format(dt.ranges[15]))
    rospy.loginfo('Range data at 345 deg:   {}'.format(dt.ranges[345]))
    rospy.loginfo('-------------------------------------------')

def turtle_mover():
    move = Twist() 

    while not rospy.is_shutdown():
        t0 = rospy.Time.now().to_sec()

        if dt is not None and dt.ranges[0] > thr1 and dt.ranges[10]>thr2 and dt.ranges[350]>thr2:
            move.linear.x = 0.2 
            move.angular.z = 0.0
            pub.publish(move)
            t0 = rospy.Time.now().to_sec()
        elif dt is None:
            move.linear.x = 0.2 
            move.angular.z = 0.0
            rospy.sleep(2)
            t0 = rospy.Time.now().to_sec()
            pub.publish(move)
        else:
            rospy.sleep(2)

            move.linear.x = 0.0 
            move.angular.z = 0.3

            t1 = rospy.Time.now().to_sec()
            pub.publish(move) 

            if (t1 - t0) * (math.radians(abs(0.5))) > 88:
                move.linear.x = 0.0
                move.angular.z = 0.0
                pub.publish(move)
                rospy.sleep(2)
                break

if __name__=="__main__":
    rospy.init_node('obstacle_avoidance_node')

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)  
    sub = rospy.Subscriber("/scan", LaserScan, callback) 
    turtle_mover()

