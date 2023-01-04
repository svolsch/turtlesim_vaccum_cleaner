#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class WallFollowingTurtle:
    def __init__(self):
        self.pose = Pose()
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)
        self.wall_distance = 1.0  # distance from the wall at which the turtle should turn

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    def move(self):
        vel_msg = Twist()
        vel_msg.linear.x = 0.5  # move forward at a constant speed

        # If the turtle is too close to the right wall, turn left
        if self.pose.x > 11 - self.wall_distance:
            vel_msg.angular.z = 0.5
        # If the turtle is too close to the left wall, turn right
        elif self.pose.x < self.wall_distance:
            vel_msg.angular.z = -0.5
        # If the turtle is not too close to either wall, go straight
        else:
            vel_msg.angular.z = 0

        self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    rospy.init_node('wall_following_turtle')
    turtle = WallFollowingTurtle()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        turtle.move()
        rate.sleep()
