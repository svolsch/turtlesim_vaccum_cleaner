#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

x1 = 0.0
y1 = 0.0
x2 = 0.0
y2 = 0.0

def callback1(data):
    global x1, y1
    x1 = data.x
    y1 = data.y

def callback2(data):
    global x2, y2
    x2 = data.x
    y2 = data.y

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def move():
    pub1 = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    pub2 = rospy.Publisher('turtle2/cmd_vel', Twist, queue_size=10)

    rospy.Subscriber("turtle1/pose", Pose, callback1)
    rospy.Subscriber("turtle2/pose", Pose, callback2)

    rospy.init_node('random_move', anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # turtle1
        vel_msg1 = Twist()
        dist1 = distance(x1, y1, x2, y2)
        if dist1 < 2:
            vel_msg1.angular.x = -3.5
            vel_msg1.linear.x = 3.5

        elif x1 <10 or y1 <10 or x1 < 2 or y1 < 2:
            vel_msg1.linear.x = 3.5
            vel_msg1.angular.z = 3.5
        else:
            vel_msg1.linear.x = 3.5
            vel_msg1.angular.z = 0
        pub1.publish(vel_msg1)

        # turtle2
        vel_msg2 = Twist()
        dist2 = distance(x2, y2, x1, y1)
        if dist2 < 2:
            vel_msg2.angular.x = -3.5
            vel_msg2.linear.x = 3.5

        elif x2 <10 or y2 <10 or x2 < 2 or y2 < 2:
            vel_msg2.linear.x = 3.5
            vel_msg2.angular.z = 3.5
        else:
            vel_msg2.linear.x = 5.5
            vel_msg2.angular.z = 0
        
        pub2.publish(vel_msg2)

        rate.sleep()

if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass
