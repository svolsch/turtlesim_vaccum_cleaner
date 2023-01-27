#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt
    
    
class navCord:
   
    def __init__(self):
        rospy.init_node('navigator', anonymous=False) #Initialize node navigator
   
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) #Publish twist msg to cmd_vel
        self.subscribe_pose = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose) #Subscriber for pose topic for turtle 1

        self.pose = Pose()
        self.rate = rospy.Rate(10)
   
    def update_pose(self, data):
           self.pose = data
           self.pose.x = round(self.pose.x, 4)
           self.pose.y = round(self.pose.y, 4)
        
    def euclidean_distance(self, goal_pose):
        return sqrt(pow((goal_pose.x - self.pose.x), 2) + pow((goal_pose.y - self.pose.y), 2))
   
    def linear_vel(self, goal_pose, constant=1.5):
        return constant * self.euclidean_distance(goal_pose)
   
    def steering_angle(self, goal_pose):
        return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
   
    def angular_vel(self, goal_pose, constant=6):
        return constant * (self.steering_angle(goal_pose) - self.pose.theta)
   
    def move_turtle(self):
           goal_pose = Pose()
   
           # Get x and y coordinates for the goal position from the user
           goal_pose.x = float(input("Set your x goal: "))
           goal_pose.y = float(input("Set your y goal: "))
   
           # Please, insert a number slightly greater than 0 (e.g. 0.01).
           distance_tolerance = float(input("Set your tolerance: ")) 
   
           vel_msg = Twist()
   
           while self.euclidean_distance(goal_pose) >= distance_tolerance:
      
               # Linear velocity in the x-axis.
               vel_msg.linear.x = self.linear_vel(goal_pose)
               vel_msg.linear.y = 0
               vel_msg.linear.z = 0
   
               # Angular velocity in the z-axis.
               vel_msg.angular.x = 0
               vel_msg.angular.y = 0
               vel_msg.angular.z = self.angular_vel(goal_pose)
   
               # Publishing our vel_msg
               self.velocity_publisher.publish(vel_msg)
   
               # Publish at the desired rate.
               self.rate.sleep()
   
           # Stop after reaching the goal position
           vel_msg.linear.x = 0
           vel_msg.angular.z = 0
           self.velocity_publisher.publish(vel_msg)
   
           # If we press control + C, the node will stop.
           rospy.spin()

    

if __name__ == '__main__':
    try:
         x = navCord()
         x.move_turtle()
    except rospy.ROSInterruptException:
         pass

