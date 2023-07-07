#!/usr/bin/env python

import rospy
from publisher_subscriber_examples.srv import lifter
from publisher_subscriber_examples.srv import lifterRequest
from publisher_subscriber_examples.srv import lifterResponse

def lifter_call_back(req):
    #kalkmadi = "kaldırılamadı"
    #kalkti = "kaldırıldı"
    value = req.value
    print("Req value: {}".format(value))
    if (value > 5):
        rospy.loginfo("1")
        return lifterResponse("kaldırılamadı")
    else:
        rospy.loginfo("2")
        return lifterResponse("kaldırıldı")

def lifter_server():
    rospy.init_node("lifter_server_node")
    service = rospy.Service("lifter_server",lifter,lifter_call_back)
    print("Server is ready")
    rospy.spin()


if __name__=="__main__":
    lifter_server()