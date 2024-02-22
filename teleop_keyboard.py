#!/usr/bin/env python3
from math import pi
import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
from ros_gz_interfaces.msg import ParamVec


import sys

class TeleopKeyboard(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')
        self.bearing=0
        self.range=0
        self.phase=1
        self.latitude=48.04631295419033
        self.longitude=-4.976315895687726

        self.main_turn_pub = self.create_publisher(Float64, '/wamv/thrusters/main/pos', 5)
        self.main_speed_pub = self.create_publisher(Float64, '/wamv/thrusters/main/thrust', 5)
        self.main_bouee=self.create_subscription(ParamVec, '/wamv/sensors/acoustics/receiver/range_bearing', self.callback, 5)



        self.get_logger().info('Teleop Keyboard Node Started')
        self.main_timer=self.create_timer(0.1,self.run)



    def callback(self,msg):
        for param in msg.params:
            if param.name=='bearing':
                self.bearing=param.value.double_value
            if param.name=='range':
                self.range=param.value.double_value




    def dir(self):
        gain=0.01
        return(min((pi/4),max((-pi/4),-gain*self.bearing)))

    def moteur(self):
        gain=50
        x=gain*self.range
        return(max(0,min(12000,x)))



    def vels(self, speed, turn):
        return "currently:\tspeed %s\tturn %s " % (speed,turn)
    
    def run(self):
        speed = 0.0
        turn = 0.0
        speed_limit = 12000.0
        turn_limit = 0.78539816339
        try:

            speed=float(self.moteur())
            turn=float(self.dir())

            print(self.vels(speed,turn))

            speed_msg = Float64()
            turn_msg = Float64()
            speed_msg.data = speed
            turn_msg.data = turn
            
            self.main_turn_pub.publish(turn_msg)
            self.main_speed_pub.publish(speed_msg)

        except Exception as e:
            print(e)


def main(args=None):
    rclpy.init(args=args)

    teleop_keyboard = TeleopKeyboard()

    rclpy.spin(teleop_keyboard)
    
    teleop_keyboard.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()