import rospy
from turtlesim.msg import ColorRGBA
from geometry_msgs.msg import Twist

# Set the color to avoid
AVOID_COLOR = ColorRGBA(r=0.8, g=0.2, b=0.2, a=1.0)

def color_sensor_callback(color):
    # Check if the turtle is over the color to avoid
    if color.r == AVOID_COLOR.r and color.g == AVOID_COLOR.g and color.b == AVOID_COLOR.b:
        # Create a Twist message to turn the turtle to the right
        twist = Twist()
        twist.angular.z = 1.0
        # Publish the Twist message to the /turtle1/cmd_vel topic
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        pub.publish(twist)

def main():
    # Initialize the ROS node
    rospy.init_node('color_avoidance')

    # Subscribe to the /turtle1/color_sensor topic
    rospy.Subscriber('/turtle1/color_sensor', ColorRGBA, color_sensor_callback)

    # Spin until the ROS node is shutdown
    rospy.spin()

if __name__ == '__main__':
    main()
