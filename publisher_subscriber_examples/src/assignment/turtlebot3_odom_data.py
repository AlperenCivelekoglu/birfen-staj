#!/usr/bin/env python

import rospy
import time
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


def pose_call_back(pose_message):
    print("------odom topic's position datas: \nx: {}\ny: {}\nz: {}".format(
    pose_message.pose.pose.position.x,
    pose_message.pose.pose.position.y,
    pose_message.pose.pose.position.z,
    ))

    print("------odom topic's orientation datas: \nx: {}\ny: {}\nz: {}\nw: {}".format(
    pose_message.pose.pose.orientation.x,
    pose_message.pose.pose.orientation.y,
    pose_message.pose.pose.orientation.z,
    pose_message.pose.pose.orientation.w))

if __name__=="__main__":
    try:
        rospy.init_node("odom_subscriber")

        odom_topic = "/odom"
        odom_subscriber = rospy.Subscriber(odom_topic,Odometry,pose_call_back)
        time.sleep(5)
        rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Interrupted")
        