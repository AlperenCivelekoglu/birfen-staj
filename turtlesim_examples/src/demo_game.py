#!/usr/bin/env python

import rospy
import time
import math
import numpy as np
from geometry_msgs.msg import Twist
import curses
import sys, select, termios, tty

lx = 0.0
ly = 0.0
lz = 0.0
ax = 0.0
ay = 0.0
az = 0.0

def get_key():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
        if key == '\x1b':
            key = sys.stdin.read(2)  # Okuma işlemi için 2 ekstra karakter alın
            if key == '[A':
                key = '\x1b[A'  # Yukarı yön tuşu
            elif key == '[B':
                key = '\x1b[B'  # Aşağı yön tuşu
            elif key == '[C':
                key = '\x1b[C'  # Sağ yön tuşu
            elif key == '[D':
                key = '\x1b[D'  # Sol yön tuşu
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key



def pose_call_back(pose_messages):
    global lx, ax, ly, ay, lz, az

    lx = pose_messages.linear.x
    ly = pose_messages.linear.y
    lz = pose_messages.linear.z

    ax = pose_messages.angular.x
    ay = pose_messages.angular.y
    az = pose_messages.angular.z

def turtle_mover(publisher, x, z):
    velocity_message = Twist()
    try:
        velocity_message.linear.x = float(x)
        velocity_message.angular.z = float(z)
    except ValueError:
        print("value error")

    publisher.publish(velocity_message)


if __name__=="__main__": 
    settings = termios.tcgetattr(sys.stdin) 
    try:
        rospy.init_node("turtle_controller")

        turtle1_cmd_vel_topic = "/turtle1/cmd_vel"
        turtle1_cmd_vel_publisher = rospy.Publisher(turtle1_cmd_vel_topic,Twist,queue_size=10)

        turtle2_cmd_vel_topic = "/turtle2/cmd_vel"
        turtle2_cmd_vel_publisher = rospy.Publisher(turtle2_cmd_vel_topic,Twist,queue_size=10)

        time.sleep(5)
        rospy.loginfo("-------------Turtle 1 commands----------\nw: Moves forward\na: turns left\ns: moves back\nd: turns right\n" +
                  "-------------Turtle 2 commands----------\n↑: Moves forward\n←: turns left\n↓: moves back\n→: turns right")
        
        while not rospy.is_shutdown():
            #rospy.loginfo("inside while loop")
            key = get_key()
            if key == "w":
                turtle_mover(turtle1_cmd_vel_publisher, 2, 0)
            elif key == "a":
                turtle_mover(turtle1_cmd_vel_publisher, 0, 0.8)
            elif key == "s":
                turtle_mover(turtle1_cmd_vel_publisher, -2, 0)
            elif key == "d":
                turtle_mover(turtle1_cmd_vel_publisher, 0, -0.8)
            elif key == '\x1b[A':
                turtle_mover(turtle2_cmd_vel_publisher, 2, 0)
            elif key == '\x1b[B':
                turtle_mover(turtle2_cmd_vel_publisher, 0, 0.8)
            elif key == '\x1b[C':
                turtle_mover(turtle2_cmd_vel_publisher, -2, 0)
            elif key == '\x1b[D':
                turtle_mover(turtle2_cmd_vel_publisher, 0, -0.8)          
    except rospy.ROSInterruptException:
        print("Interrupted")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
