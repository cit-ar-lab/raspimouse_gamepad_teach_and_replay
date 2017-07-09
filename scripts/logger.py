#!/usr/bin/env python
# Copyright 2017 Masahiro Kato
# Copyright 2017 Ryuichi Ueda
# Released under the BSD License.

import rospy, math, sys, random
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse
from raspimouse_ros_2.msg import LightSensorValues
from raspimouse_gamepad_training_replay.msg import Event

class Logger():
    def __init__(self):
        self.decision = rospy.Publisher('/event',Event,queue_size=100)

        self.sensor_values = LightSensorValues()
        rospy.Subscriber('/lightsensors', LightSensorValues, self.callback)

        self.cmd_vel = Twist()
        rospy.Subscriber('/cmd_vel', Twist, self.callback2)

    def callback(self,messages):
        self.sensor_values = messages

    def callback2(self,messages):
        self.cmd_vel = messages

    def output_decision(self):
	s = self.sensor_values
	a = self.cmd_vel
	e = Event()

        e.left_side = s.left_side
        e.right_side = s.right_side
        e.left_forward = s.left_forward
        e.right_forward = s.right_forward
        e.linear_x = a.linear.x
        e.angular_z = a.angular.z

        self.decision.publish(e)

    def run(self):
        rate = rospy.Rate(10)
        data = Twist()

        while not rospy.is_shutdown():
            self.output_decision()
            rate.sleep()

if __name__ == '__main__':
    rospy.init_node('logger')
    Logger().run()
