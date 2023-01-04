#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

def callback(data):
    # Get the current position and orientation of the turtle
    x = data.x
    y = data.y
    theta = data.theta

    # Check if the turtle is too close to a wall
    if x < 1 or x > 10 or y < 1 or y > 10:
        # If so, turn the turtle away from the wall
        if x < 1:
            # Turn to the right if too close to the left wall
            pub.publish(0, 0, -0.5)
        elif x > 10:
            # Turn to the left if too close to the right wall
            pub.publish(0, 0, 0.5)
        elif y < 1:
            # Turn to the right if too close to the bottom wall
            pub.publish(0, 0, 0.5)
        elif y > 10:
            # Turn to the left if too close to the top wall
            pub.publish(0, 0, -0.5)
    else:
        # If not too close to a wall, move straight ahead
        pub.publish(1, 0, 0)

def main():
    # Initialize the node and subscriber
    rospy.init_node('wall_avoidance')
    sub = rospy.Subscriber('turtle1/pose', Pose, callback)

    # Create a publisher for the turtle's velocity
    global pub
    pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)

    # Spin until the node is shut down
    rospy.spin()

if __name__ == '__main__':
    main()
