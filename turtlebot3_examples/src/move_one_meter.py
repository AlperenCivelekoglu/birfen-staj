#!/usr/bin/env python

import rospy
import time
import math
import numpy as np
from geometry_msgs.msg import Twist

def turtlebot_mover(publisher, distance, speed):
    velocity_message = Twist()
    
    distance_moved = 0
    loop_rate = rospy.Rate(10)
    
    t0 = rospy.Time.now().to_sec()

    while distance_moved < distance:
        rospy.loginfo("Turtlesim moves forward")
        velocity_message.linear.x = speed
        publisher.publish(velocity_message)
        
        t1 = rospy.Time.now().to_sec()
        distance_moved = speed * (t1 - t0)

        loop_rate.sleep()
    
    velocity_message.linear.x = 0
    publisher.publish(velocity_message)


if __name__ == "__main__":
    rospy.init_node("turtlebot_controller")
    
    try:
        turtlebot_cmdvel_topic = "/cmd_vel"
        turtlebot_cmdvel_publisher = rospy.Publisher(turtlebot_cmdvel_topic, Twist, queue_size=10)
        time.sleep(5)

        turtlebot_mover(turtlebot_cmdvel_publisher, 1, 0.5)
    except rospy.ROSInterruptException:
        print("Interrupted") 
