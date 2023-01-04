#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen
from turtlesim.srv import TeleportRelative
from turtlesim.srv import Spawn
from turtlesim.msg import Pose

# Initialize the node
rospy.init_node('avoid_walls_turtle')

# Spawn a new turtle
rospy.wait_for_service('spawn')
spawner = rospy.ServiceProxy('spawn', Spawn)
spawner(4, 2, 0, 'my_turtle')

# Set the pen color to green
rospy.wait_for_service('turtle1/set_pen')
set_pen = rospy.ServiceProxy('turtle1/set_pen', SetPen)
set_pen(0, 255, 0, 2, False)

# Teleport the turtle to the center of the screen
rospy.wait_for_service('turtle1/teleport_absolute')
teleporter = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
teleporter(5.544445, 5.544445, 0)

# Create a subscriber to listen for pose updates
def pose_callback(pose):
    # Check if the turtle is near a wall
    if pose.x < 0.1 or pose.x > 10.9 or pose.y < 0.1 or pose.y > 10.9:
        # Teleport the turtle to the opposite side of the screen
        teleporter(10.9 - pose.x, 10.9 - pose.y, pose.theta)

rospy.Subscriber('turtle1/pose', Pose, pose_callback)

# Spin to keep the node alive
rospy.spin()
