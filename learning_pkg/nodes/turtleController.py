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

class turtleCleaners:
    def __init__(self):
        self.pose = Pose()

        # Publish to cmd_vel for turtle 1,2 and 3
        self.velocity_publisher1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) 
        self.velocity_publisher2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10) 
        self.velocity_publisher3 = rospy.Publisher('/turtle3/cmd_vel', Twist, queue_size=10) 
        
        # Subscribe to turtle 1,2 and 3's pose
        self.turtle1_pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.turtle1_pose_callback)
        self.turtle2_pose_subscriber = rospy.Subscriber('/turtle2/pose', Pose, self.turtle2_pose_callback)
        self.turtle3_pose_subscriber = rospy.Subscriber('/turtle3/pose', Pose, self.turtle3_pose_callback)

        self.set_pen_color(255, 255, 255)  # set pen color to white
        
    #Turtle 1 callback function 
    def turtle1_pose_callback(self,pose):
        self.turtle1_x = round(pose.x, 1)
        self.turtle1_y = round(pose.y, 1)
    #Turtle 2 callback function
    def turtle2_pose_callback(self,pose):
        self.turtle2_x = round(pose.x, 1)
        self.turtle2_y = round(pose.y, 1)
    #Turtle 3 callback function     
    def turtle3_pose_callback(self,pose):
        self.turtle3_x = round(pose.x, 1)
        self.turtle3_y = round(pose.y, 1)
    
    #Function to change the pen color to white for turtles 1,2,3
    def set_pen_color(self, r, g, b):
        rospy.wait_for_service('turtle1/set_pen')
        rospy.wait_for_service('turtle2/set_pen')
        rospy.wait_for_service('turtle3/set_pen')
        try:
            pen_servicet1 = rospy.ServiceProxy('turtle1/set_pen', SetPen)
            pen_servicet2 = rospy.ServiceProxy('turtle2/set_pen', SetPen)
            pen_servicet3 = rospy.ServiceProxy('turtle3/set_pen', SetPen)
            pen_servicet1(r, g, b, 30, 0)
            pen_servicet2(r, g, b, 30, 0)
            pen_servicet3(r, g, b, 30, 0)
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
    # Motion Control for turtle 1
    def move_turtle1(self):
        vel_msg = Twist()
        lin_vel = 3.5
        ang_vel = 3.5
        dist12 = abs(math.sqrt((self.turtle2_x - self.turtle1_x)**2 + (self.turtle2_y - self.turtle1_y)**2))
        dist13 = abs(math.sqrt((self.turtle3_x - self.turtle1_x)**2 + (self.turtle3_y - self.turtle1_y)**2))

        # If distance between turtle 1 and turtle 2 is less than 3.0 move around
        if dist12 < 2.0:
            
            vel_msg.angular.z = -ang_vel
            vel_msg.linear.x = lin_vel

        # If distance between turtle 1 and turtle 3 is less than 3.0 move around
        elif dist13 < 2.0:
            
            vel_msg.angular.z = -ang_vel
            vel_msg.linear.x = lin_vel

        # Move around if the distance between turtle 1 and the walls is less than 1.0
        elif self.turtle1_x > 10.0 or self.turtle1_y > 10.0 or self.turtle1_x < 1.0 or self.turtle1_y < 1.0:
            
            vel_msg.angular.z = -ang_vel
            vel_msg.linear.x = lin_vel

        # If the turtle is not too close to either wall or any other turtles, go straight
        else:

            vel_msg.angular.z = 0
            vel_msg.linear.x = lin_vel
            


        self.velocity_publisher1.publish(vel_msg)
    
    # Motion control for turtle 2
    def move_turtle2(self):
        vel_msg_2 = Twist()
        lin_vel = 3.5
        ang_vel = 3.5
        dist21 = abs(math.sqrt((self.turtle2_x - self.turtle1_x)**2 + (self.turtle2_y - self.turtle1_y)**2))
        dist23 = abs(math.sqrt((self.turtle3_x - self.turtle2_x)**2 + (self.turtle3_y - self.turtle2_y)**2))

        # If distance between turtle 2 and turtle 1 is less than 3.0 move around
        if  dist21 < 2.0:
            
            vel_msg_2.angular.z = ang_vel
            vel_msg_2.linear.x = lin_vel

        # If distance between turtle 2 and turtle 3 is less than 3.0 move around
        elif dist23 < 2.0:
            
            vel_msg_2.angular.z = ang_vel
            vel_msg_2.linear.x = lin_vel

        # Move around if the distance between turtle 2 and the walls is less than 1.0
        elif self.turtle2_x > 10.0 or self.turtle2_y > 10.0 or self.turtle2_x < 1.0 or self.turtle2_y < 1.0:
            
            vel_msg_2.angular.z = ang_vel
            vel_msg_2.linear.x = lin_vel
        


        # If the turtle is not too close to either wall or any other turtles, go straight
        else:
            vel_msg_2.angular.z = 0
            vel_msg_2.linear.x = lin_vel
            


        self.velocity_publisher2.publish(vel_msg_2)

    #Motion control for turtle 3
    def move_turtle3(self):
        vel_msg_3 = Twist()
        lin_vel = 3.5
        ang_vel = 3.5
        dist31 = abs(math.sqrt((self.turtle3_x - self.turtle1_x)**2 + (self.turtle3_y - self.turtle1_y)**2))
        dist32 = abs(math.sqrt((self.turtle3_x - self.turtle2_x)**2 + (self.turtle3_y - self.turtle2_y)**2))

        ## If distance between turtle 3 and turtle 1 is less than 3.0 move around
        if dist31 < 2.0:

            vel_msg_3.angular.z = -ang_vel
            vel_msg_3.linear.x = lin_vel
            
        # If distance between turtle 3 and turtle 2 is less than 3.0 move around
        elif dist32 < 2.0:

            vel_msg_3.angular.z = ang_vel
            vel_msg_3.linear.x = lin_vel

        # Move around if the distance between turtle 3 and the walls is less than 1.0
        elif self.turtle3_x > 10.0 or self.turtle3_y > 10.0 or self.turtle3_x < 1.0 or self.turtle3_y < 1.0:
            vel_msg_3.angular.z = -ang_vel
            vel_msg_3.linear.x = lin_vel
        

    
        # If the turtle is not too close to either wall or any other turtles, go straight
        else:
            vel_msg_3.angular.z = 0
            vel_msg_3.linear.x = lin_vel
            


        self.velocity_publisher3.publish(vel_msg_3)

if __name__ == '__main__':
    rospy.init_node('explorer_turtles')
    turtle = turtleCleaners()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        turtle.move_turtle1() # Start moving turtle 1
        turtle.move_turtle2() # Start moving turtle 2
        turtle.move_turtle3() # Start moving turtle 3
        rate.sleep()
