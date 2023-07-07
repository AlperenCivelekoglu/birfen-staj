#!/usr/bin/env python

import rospy
import sys
from publisher_subscriber_examples.srv import lifter
from publisher_subscriber_examples.srv import lifterRequest
from publisher_subscriber_examples.srv import lifterResponse

def lifter_request(value):
    rospy.loginfo("Waiting for server")
    rospy.wait_for_service("lifter_server")
    
    try:
        proxy = rospy.ServiceProxy("lifter_server",lifter)
        server_response = proxy(int(value))
        return server_response.output
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def usage():
    return "%s [value]"%sys.argv[0]

if __name__=="__main__":
    if len(sys.argv)==2:
        value = int(sys.argv[1])
    else:
        print(usage())
        sys.exit(1)
    response = lifter_request(value)
    print(response)
