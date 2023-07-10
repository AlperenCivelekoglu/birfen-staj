#!/usr/bin/env python

import rospy
import time
import math
import numpy as np
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

x = 0.0
y = 0.0
yaw = 0.0
ax = 0.0

x0 = 0.0
y0 = 0.0
yaw0 = 0.0

def pose_callback(pose_message):
    global x, y, yaw

    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

def move(publisher, speed, angular_speed,distance, is_forward):
        #declare a Twist message to send velocity commands
        velocity_message = Twist()
        #get current location 
        global x, y
        x0=x
        y0=y

        if (is_forward):
            velocity_message.linear.x =abs(speed)
        else:velocity_message.linear.x =-abs(speed)
        velocity_message.angular.x = angular_speed

        distance_moved = 0.0
        loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
        
        if angular_speed == 0:
            while True :
                rospy.loginfo("Turtlesim moves forwards")
                publisher.publish(velocity_message)

                loop_rate.sleep()
                
                distance_moved = abs(math.sqrt(((x-x0) ** 2) + ((y-y0) ** 2)))
                print (distance_moved)
                print(x)
                if  not (distance_moved<distance):
                    rospy.loginfo("reached")
                    break
        else:
            while True :
                publisher.publish(velocity_message)
                loop_rate.sleep()
                
        #finally, stop the robot when the distance is moved
        velocity_message.linear.x =0
        publisher.publish(velocity_message)

def rotate (publisher, angular_speed_degree, relative_angle_degree, clockwise):
    
    velocity_message = Twist()

    angular_speed=math.radians(abs(angular_speed_degree))

    if (clockwise):
        velocity_message.angular.z =-abs(angular_speed)
    else:
        velocity_message.angular.z =abs(angular_speed)

    angle_moved = 0.0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times a second)    
    cmd_vel_topic='/turtle1/cmd_vel'
    publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t0 = rospy.Time.now().to_sec()

    while True :
        rospy.loginfo("Turtlesim rotates")
        publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1-t0)*angular_speed_degree
        loop_rate.sleep()


                       
        if  (current_angle_degree>relative_angle_degree):
            rospy.loginfo("reached")
            break

def turtle_mover(publisher, shape):
    global x, y, yaw

    if shape == "üçgen":
        side_length = 2.0
        for _ in range(3):
            move(publisher, 1.0, 0.0, side_length, True)
            rotate(publisher, 45, 120, False)

    elif shape == "kare":
        side_length = 2.0
        for _ in range(4):
            move(publisher, 1.0, 0.0, side_length, True)
            rotate(publisher, 9, 90, False)

    elif shape == "yuvarlak":
        #radius = 0.2
        #circumference = 2 * math.pi * radius
        move(publisher, 0.8, 0.4, 0, True)

    else:
        rospy.logwarn("Invalid shape input!")

    stop_moving(publisher)

def stop_moving(publisher):
    velocity_message = Twist()
    velocity_message.linear.x = 0.0
    velocity_message.angular.z = 0.0
    publisher.publish(velocity_message)


if __name__ == "__main__":
    try:
        rospy.init_node("turtle_controller")

        turtle1_cmd_vel_topic = "/turtle1/cmd_vel"
        turtle1_cmd_vel_publisher = rospy.Publisher(turtle1_cmd_vel_topic, Twist, queue_size=10)

        turtle1_pose_topic = "/turtle1/pose"
        turtle1_pose_subscriber = rospy.Subscriber(turtle1_pose_topic, Pose, pose_callback)
        time.sleep(5)

        rospy.loginfo("Please select shape (üçgen, kare, yuvarlak):")
        shape = input()

        turtle_mover(turtle1_cmd_vel_publisher, shape)

    except rospy.ROSInterruptException:
        print("Interrupted")
