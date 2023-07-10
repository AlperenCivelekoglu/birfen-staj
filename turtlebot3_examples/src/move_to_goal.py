#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
from nav_msgs.msg import Odometry


xi = 0.0
yi = 0.0
yawi = 0.0

def poseCallback(pose_message):
    global xi, yi, yawi
    xi = pose_message.pose.pose.position.x
    yi = pose_message.pose.pose.position.y
    yawi = pose_message.pose.pose.orientation.z


def go_to_goal(velocity_publisher, x_goal, y_goal):
    global xi, yi, yawi

    velocity_message = Twist()

    while True:
        K_linear = 0.5 
        distance = abs(math.sqrt((x_goal - xi)**2 + (y_goal - yi)**2))

        linear_speed = distance * K_linear

        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal - yi, x_goal - xi)
        angular_speed = (desired_angle_goal - yawi) * K_angular

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        velocity_publisher.publish(velocity_message)
        print("x = {}, y = {}, distance to goal: {}".format(xi, yi, distance))

        if distance < 0.01:
            break

if __name__ == "__main__":
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        # Declare velocity publisher
        cmd_vel_topic = "/cmd_vel"
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        position_topic = "/odom"
        pose_subscriber = rospy.Subscriber(position_topic,Odometry, poseCallback)

        time.sleep(5)

        rospy.loginfo("Please type goal coordinates x, y")
        a, b = map(float, input().split())

        go_to_goal(velocity_publisher, a, b)
    except rospy.ROSInterruptException:
        pass
