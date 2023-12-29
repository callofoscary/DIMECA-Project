#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist

def joy_callback(msg):
    # Procesar los mensajes de joystick y generar mensajes de velocidad
    linear_x = scale(msg.axes[1], -1.0, 1.0, -2.0, 2.0)
    angular_z = scale(msg.axes[2], -1.0, 1.0, -2.0, 2.0)

    twist_msg = Twist()
    twist_msg.linear.x = linear_x
    twist_msg.angular.z = angular_z

    # Publicar mensaje de velocidad
    pub.publish(twist_msg)

def scale(value, in_min, in_max, out_min, out_max):
    # Función para escalar valores de entrada a un rango deseado
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

if __name__ == "__main__":
    rospy.init_node("ds4_control_node")
    rospy.loginfo("DS4 Control Node Started")

    pub = rospy.Publisher("/mobile_base_controller/cmd_vel", Twist, queue_size=10)
    rospy.Subscriber("/joy", Joy, joy_callback)

    rospy.spin()
