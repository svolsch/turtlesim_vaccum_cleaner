#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
import random
import time
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen

class WallAvoidingTurtle:
    def __init__(self):
        self.pose = Pose()

        self.turtle1_pose = rospy.wait_for_message('/turtle' + str(1) + '/pose', Pose)
        self.turtle2_pose = rospy.wait_for_message('/turtle' + str(2) + '/pose', Pose)
        self.turtle3_pose = rospy.wait_for_message('/turtle' + str(3) + '/pose', Pose)

        self.velocity_publisher = rospy.Publisher('/turtle4/cmd_vel', Twist, queue_size=10)

        self.pose_publisher_1 = rospy.Publisher('/turtle1/pose', Pose, queue_size = 10)
        self.pose_publisher_2 = rospy.Publisher('/turtle2/pose', Pose, queue_size = 10)
        self.pose_publisher_3 = rospy.Publisher('/turtle3/pose', Pose, queue_size = 10)

        self.pose_subscriber = rospy.Subscriber('/turtle4/pose', Pose, self.update_pose)
        self.pose_subscriber1 = rospy.Subscriber('/turtle1/pose', Pose, self.pose_callback)
        self.pose_subscriber2 = rospy.Subscriber('/turtle2/pose', Pose, self.pose_callback)
        self.pose_subscriber3 = rospy.Subscriber('/turtle3/pose', Pose, self.pose_callback)
        self.wall_distance = 1.0  # distance from the wall at which the turtle should turn
        self.set_pen_color(255, 255, 255)  # set pen color to white

    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
    
    def pose_callback(self,msg):
        vel_msg=Twist()
    # Check if the x and y position of the two turtles are the same
        if msg.x == self.turtle1_pose.x and msg.y == self.turtle1_pose.y:
            rospy.loginfo("Turtle 1 and 4 collision ")
            vel_msg.linear.x = 0.5
            vel_msg.angular.z = 2.0
        elif msg.x == self.turtle2_pose.x and msg.y == self.turtle2_pose.y:
            rospy.loginfo("Turtle 2 and 4 collision")
            vel_msg.linear.x = 0.5
            vel_msg.angular.z = 2.0
        elif msg.x == self.turtle3_pose.x and msg.y == self.turtle3_pose.y:
            rospy.loginfo("Turtle 3 and 4 collision")
            vel_msg.linear.x = 0.5
            vel_msg.angular.z = 2.0

    def set_pen_color(self, r, g, b):
        rospy.wait_for_service('turtle4/set_pen')
        try:
            pen_service = rospy.ServiceProxy('turtle4/set_pen', SetPen)
            pen_service(r, g, b, 30, 0)
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)

    def move(self):
        vel_msg = Twist()
        lin_vel = 3.5
        ang_vel = random.choice([3.5, -3.5])

        # If the turtle is too close to the right wall, turn left
        if self.pose.x > 11 - self.wall_distance:
            vel_msg.linear.x = 0.0
            time.sleep(1)
            vel_msg.angular.z = ang_vel
            vel_msg.linear.x = lin_vel
        elif self.pose.y > 11 - self.wall_distance:
            vel_msg.linear.x = 0.0
            time.sleep(1)
            vel_msg.angular.z = ang_vel
            vel_msg.linear.x = lin_vel
            
        elif self.pose.y < self.wall_distance:
            vel_msg.linear.x = 0.0
            time.sleep(1)
            vel_msg.angular.z = ang_vel
            vel_msg.linear.x = lin_vel
            
        # If the turtle is too close to the left wall, turn right
        elif self.pose.x <  self.wall_distance:
            vel_msg.linear.x = 0.0
            time.sleep(1)
            vel_msg.angular.z = ang_vel
            vel_msg.linear.x = lin_vel
            
        # If the turtle is not too close to either wall, go straight
        else:
            vel_msg.angular.z = 0
            vel_msg.linear.x = lin_vel
            


        self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    rospy.init_node('wall_avoiding_turtle')
    turtle = WallAvoidingTurtle()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        turtle.move()
        rate.sleep()
