#!/usr/bin/env python  
import roslib
roslib.load_manifest('learning_pkg')
import rospy
from geometry_msgs.msg import Twist
from pynput import keyboard

def on_press(key):
    global pub
    global turtle_vel
    global lin_vel
    global ang_vel
    if key == keyboard.Key.up:
        turtle_vel.linear.x = lin_vel
    elif key == keyboard.Key.down:
        turtle_vel.linear.x = -lin_vel
    elif key == keyboard.Key.left:
        turtle_vel.angular.z = -ang_vel
    elif key == keyboard.Key.right:
        turtle_vel.angular.z = ang_vel
    pub.publish(turtle_vel)

def on_release(key):
    global pub
    global turtle_vel
    if key == keyboard.Key.up or key == keyboard.Key.down:
        turtle_vel.linear.x = 0
    elif key == keyboard.Key.left or key == keyboard.Key.right:
        turtle_vel.angular.z = 0
    pub.publish(turtle_vel)

def turtle_keyboard():
    global pub
    global turtle_vel
    global lin_vel
    global ang_vel
    rospy.init_node('turtle_keyboard')
    lin_vel = float(input("Enter the linear speed for this session: "))
    ang_vel = float(input("Enter the angular velocity for this session: "))
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    turtle_vel = Twist()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == '__main__':
    try:
        turtle_keyboard()
    except rospy.ROSInterruptException:
        pass
