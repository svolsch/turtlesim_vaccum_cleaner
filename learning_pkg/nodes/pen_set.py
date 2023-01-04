#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from turtlesim.srv import SetPen

def set_pen_width(width):
    rospy.wait_for_service('turtle1/set_pen')
    try:
        pen_service = rospy.ServiceProxy('turtle1/set_pen', SetPen)
        pen_service(255, 255, 255, width, 0)
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

if __name__ == '__main__':
    rospy.init_node('pen_width_changer')

    # Set the pen width to 10
    set_pen_width(20)
