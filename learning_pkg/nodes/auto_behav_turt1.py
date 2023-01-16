#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
import random
import time
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from turtlesim.srv import Spawn

class WallAvoidingTurtle:
    def __init__(self):
        self.pose = Pose()
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.pose_publisher_2 = rospy.Publisher('/turtle1/pose', Pose, queue_size = 10)

        self.turtle1_pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.turtle1_pose_callback)
        self.turtle2_pose_subscriber = rospy.Subscriber('/turtle2/pose', Pose, self.turtle2_pose_callback)
        
        # self.wall_distance = 1.0  # distance from the wall at which the turtle should turn
        self.set_pen_color(255, 255, 255)  # set pen color to white

    def turtle1_pose_callback(self,data):
        self.pose = data
        self.x1 = round(self.pose.x,4)
        self.y1 = round(self.pose.y,4)

    def turtle2_pose_callback(self,data):
        self.x2 = round(data.x,4)
        self.y2 = round(data.y,4)

    def set_pen_color(self, r, g, b):
        rospy.wait_for_service('turtle1/set_pen')
        try:
            pen_service = rospy.ServiceProxy('turtle1/set_pen', SetPen)
            pen_service(r, g, b, 30, 0)
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

    def move(self):
        vel_msg = Twist()
        lin_vel = 10.0
        ang_vel = random.choice([5.0,-5.0])
        vel_msg.linear.x = lin_vel
        

        # If the turtle is too close to a wall, turn in a random direction
        if math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2) < 1.0:
            # vel_msg.linear.x = 1.0
            # time.sleep(0.5)
            vel_msg.angular.z = 3.5
            vel_msg.linear.x = lin_vel
        
        elif self.x1 > 8.0 or self.y1 > 8.0 or self.x1 < 3.0 or self.y1 < 3.0:
            time.sleep(0.5)
            vel_msg.angular.z = ang_vel
            vel_msg.linear.x = lin_vel

            
        # If the turtle is not too close to either wall, go straight
        else:
            vel_msg.angular.z = 0
        
        self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    rospy.init_node('wall_avoiding_turtle')
    turtle = WallAvoidingTurtle()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        turtle.move()
        rate.sleep()
