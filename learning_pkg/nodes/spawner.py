#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from turtlesim.srv import Spawn

def spawn_turtle(x, y, theta):
    rospy.wait_for_service('spawn')
    try:
        spawner = rospy.ServiceProxy('spawn', Spawn)
        new_turtle = spawner(x, y, theta, "")
        return new_turtle.name
    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)

if __name__ == '__main__':
    rospy.init_node('turtle_spawner')

    # Spawn four turtles at different locations
    turtle2= spawn_turtle(6.5, 5.5, 1.57)
    turtle3 = spawn_turtle(4.5, 5.5, 3.14)
    turtle4 = spawn_turtle(5.5, 6.5, -1.57)

    print("Spawned turtles with names:", turtle2, turtle3, turtle4)
