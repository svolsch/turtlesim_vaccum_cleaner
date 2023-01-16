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

        self.velocity_publisher1 = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.velocity_publisher2 = rospy.Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
        self.velocity_publisher3 = rospy.Publisher('/turtle3/cmd_vel', Twist, queue_size=10)
        # self.pose_publisher_2 = rospy.Publisher('/turtle1/pose', Pose, queue_size = 10)

        self.turtle1_pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.turtle1_pose_callback)
        self.turtle2_pose_subscriber = rospy.Subscriber('/turtle2/pose', Pose, self.turtle2_pose_callback)
        self.turtle3_pose_subscriber = rospy.Subscriber('/turtle3/pose', Pose, self.turtle3_pose_callback)
        self.wall_distance = 1.0  # distance from the wall at which the turtle should turn
        self.set_pen_color(255, 255, 255)  # set pen color to white
        

    # def update_pose(self, data):
    #     self.pose = data
    #     self.pose.x = round(self.pose.x, 4)
    #     self.pose.y = round(self.pose.y, 4)

    def turtle1_pose_callback(self,pose):
        self.turtle1_x = round(pose.x, 1)
        self.turtle1_y = round(pose.y, 1)

    def turtle2_pose_callback(self,pose):
        self.turtle2_x = round(pose.x, 1)
        self.turtle2_y = round(pose.y, 1)
    
    def turtle3_pose_callback(self,pose):
        self.turtle3_x = round(pose.x, 1)
        self.turtle3_y = round(pose.y, 1)
    
    
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

    def move_turtle1(self):
        vel_msg = Twist()
        lin_vel = 3.5
        ang_vel = random.choice([3.5, -3.5])

        # If the turtle is too close to a wall, turn in a random direction
        if abs(math.sqrt((self.turtle2_x - self.turtle1_x)**2 + (self.turtle2_y - self.turtle1_y)**2)) < 3.0:
            # vel_msg.linear.x = 1.0
            # time.sleep(0.5)
            vel_msg.angular.z = 3.5
            vel_msg.linear.x = 3.5

        elif abs(math.sqrt((self.turtle3_x - self.turtle1_x)**2 + (self.turtle3_y - self.turtle1_y)**2)) < 3.0:
            # vel_msg.linear.x = 1.0
            # time.sleep(0.5)
            vel_msg.angular.z = -3.5
            vel_msg.linear.x = 3.5
        
        elif self.turtle1_x > 10.0 or self.turtle1_y > 10.0 or self.turtle1_x < 1.0 or self.turtle1_y < 1.0:
            # time.sleep(0.5)
            vel_msg.angular.z = 3.5
            vel_msg.linear.x = lin_vel

            
        # If the turtle is not too close to either wall, go straight
        else:
            vel_msg.angular.z = 0
            vel_msg.linear.x = lin_vel
            


        self.velocity_publisher1.publish(vel_msg)
    
    def move_turtle2(self):
        vel_msg_2 = Twist()
        lin_vel = 3.5
        ang_vel = random.choice([3.5, -3.5])

        # If the turtle is too close to a wall, turn in a random direction
        if abs(math.sqrt((self.turtle2_x - self.turtle1_x)**2 + (self.turtle2_y - self.turtle1_y)**2)) < 3.0:
            # vel_msg.linear.x = 1.0
            # time.sleep(0.5)
            vel_msg_2.angular.z = -3.5
            vel_msg_2.linear.x = 3.5
        
        elif abs(math.sqrt((self.turtle3_x - self.turtle2_x)**2 + (self.turtle3_y - self.turtle2_y)**2)) < 3.0:
            # vel_msg.linear.x = 1.0
            # time.sleep(0.5)
            vel_msg_2.angular.z = 3.5
            vel_msg_2.linear.x = 3.5
        
        elif self.turtle2_x > 10.0 or self.turtle2_y > 10.0 or self.turtle2_x < 1.0 or self.turtle2_y < 1.0:
            # time.sleep(0.5)
            vel_msg_2.angular.z = -3.5
            vel_msg_2.linear.x = lin_vel
        

    
        # If the turtle is not too close to either wall, go straight
        else:
            vel_msg_2.angular.z = 0
            vel_msg_2.linear.x = lin_vel
            


        self.velocity_publisher2.publish(vel_msg_2)

    def move_turtle3(self):
        vel_msg_3 = Twist()
        lin_vel = 3.5
        ang_vel = random.choice([3.5, -3.5])

        # If the turtle is too close to a wall, turn in a random direction
        if abs(math.sqrt((self.turtle3_x - self.turtle1_x)**2 + (self.turtle3_y - self.turtle1_y)**2)) < 3.0:
            vel_msg_3.angular.z = 3.5
            vel_msg_3.linear.x = 3.5
        
        elif abs(math.sqrt((self.turtle3_x - self.turtle2_x)**2 + (self.turtle3_y - self.turtle2_y)**2)) < 3.0:
            vel_msg_3.angular.z = -3.5
            vel_msg_3.linear.x = 3.5

        elif self.turtle3_x > 10.0 or self.turtle3_y > 10.0 or self.turtle3_x < 1.0 or self.turtle3_y < 1.0:
            vel_msg_3.angular.z = 3.5
            vel_msg_3.linear.x = lin_vel
        

    
        # If the turtle is not too close to either wall, go straight
        else:
            vel_msg_3.angular.z = 0
            vel_msg_3.linear.x = lin_vel
            


        self.velocity_publisher3.publish(vel_msg_3)

if __name__ == '__main__':
    rospy.init_node('wall_avoiding_turtle')
    turtle = WallAvoidingTurtle()
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        turtle.move_turtle1()
        turtle.move_turtle2()
        turtle.move_turtle3()
        rate.sleep()
