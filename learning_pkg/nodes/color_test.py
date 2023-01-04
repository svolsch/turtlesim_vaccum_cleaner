#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class ColorSensingTurtle:
    def __init__(self):
        self.color_subscriber = rospy.Subscriber('/turtle1/color_sensor', String, self.process_color)
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    def process_color(self, data):
        if data.data == "white":
            vel_msg = Twist()
            vel_msg.angular.z = 1.0  # turn at a constant speed
            self.velocity_publisher.publish(vel_msg)
        else:
            # If the color is not white, stop turning
            vel_msg = Twist()
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)

if __name__ == '__main__':
    rospy.init_node('color_sensing_turtle')
    turtle = ColorSensingTurtle()
    rospy.spin()
