#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import tty
import termios

def getKey():
    """Get a single character from the terminal."""
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def send_cmd():
    """Read keyboard input and send Twist commands."""
    rospy.init_node('keyboard_teleop', anonymous=True)
    pub = rospy.Publisher('/mobile_base_controller/cmd_vel', Twist, queue_size=10)

    twist = Twist()
    rate = rospy.Rate(10)  # 10 Hz

    print("Use WASD keys to control the robot. Press 'q' to exit.")

    while not rospy.is_shutdown():
        key = getKey()
        twist.linear.x = 0.0
        twist.angular.z = 0.0

        if key == 'w':
            twist.linear.x = 2.0
        elif key == 's':
            twist.linear.x = -2.0
        elif key == 'a':
            twist.angular.z = 2.0
        elif key == 'd':
            twist.angular.z = -2.0

        pub.publish(twist)
        rate.sleep()

        if key == 'q':
            break

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    try:
        send_cmd()
    except rospy.ROSInterruptException:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
