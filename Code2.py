#!/usr/bin/env python3
from math import *
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix, Image, CameraInfo
from std_msgs.msg import Float64
from std_msgs.msg import UInt32
import subprocess

from ros_gz_interfaces.msg import ParamVec

import sys, select, termios, tty

class TeleopKeyboard(Node):
    def __init__(self):
        super().__init__('teleop_keyboard')
        self.rviz_process = None
        self.bearing=0
        self.range=500
        self.phase=1
        self.xphase=20
        self.latitude=48.04631295419033
        self.longitude=-4.976315895687726
        self.main_turn_pub = self.create_publisher(Float64, '/wamv/thrusters/main/pos', 5)
        self.main_speed_pub = self.create_publisher(Float64, '/wamv/thrusters/main/thrust', 5)
        self.main_bouee=self.create_subscription(ParamVec, '/wamv/sensors/acoustics/receiver/range_bearing',self.callback,5)
        self.main_phase=self.create_subscription(UInt32, '/vrx/patrolandfollow/current_phase',self.callback_phase,5)
        self.main_gps=self.create_subscription(NavSatFix,'/wamv/sensors/gps/gps/fix',self.callback_gps,5)

        # self.main_cam_img=self.create_subscription(Image,'/wamv/sensors/cameras/main_camera_sensor/image_raw',self.callback_img,5)
        # self.main_cam_inf=self.create_subscription(CameraInfo,'/wamv/sensors/cameras/main_camera_sensor/camera_info',self.callback_inf,5)

        self.get_logger().info('Teleop Keyboard Node Started')
        self.main_timer=self.create_timer(0.1,self.run)

    def callback(self,msg):
        for param in msg.params:
            if param.name=='bearing':
                self.bearing=param.value.double_value
            if param.name=='range':
                self.range=param.value.double_value
        
    def callback_gps(self,msg):
        self.latitude=msg.latitude
        self.longitude=msg.longitude

    def callback_phase(self,msg):
        self.phase=msg.data
    
    # def callback_img(self,msg):
    
    # def callback_inf(self,msg):







    def vels(self, speed, turn):
        return "currently:\tspeed %s\tturn %s " % (speed,turn)
    
    def mot(self):
        gain=50
        return max(0,min(12000,gain*(self.range-self.xphase)))

    def dir(self):
        gain=0.01
        return min(pi/4,max(-pi/4,-gain*self.bearing))
    
    def mot1_2(self):
        return(3000)

    def dir1_2(self):
        gain=0.01
        return min(pi/4,max(-pi/4, gain* (self.bearing+pi)))
    


    def run(self):
        speed = 0.0
        turn = 0.0
        speed_limit = 12000.0
        turn_limit = 0.78539816339

        latitude_bouée=48.04804519121044
        longitude_bouee=-4.97550180409336
        x=50
        image_topic = "/wamv/sensors/cameras/main_camera_sensor/image_raw" 
        rviz_command = f"ros2 run rviz2 rviz2 --ros-args -p Image:=/{image_topic}"

        
        if self.rviz_process is None or self.rviz_process.poll() is not None:
            self.rviz_process = subprocess.Popen(rviz_command, shell=True)
        
        try:
            print (self.latitude)
            print(self.longitude)
            if self.phase ==1 :
                speed=float(self.mot())
                turn=float(self.dir())
                print(self.vels(speed,turn))
                print('phase=1')
                speed_msg = Float64()
                turn_msg = Float64()
                speed_msg.data = speed
                turn_msg.data = turn
        
                self.main_turn_pub.publish(turn_msg)
                self.main_speed_pub.publish(speed_msg)

            elif self.phase == 2 : 
                if self.range < x :
                    speed=float(self.mot1_2())
                    turn=float(self.dir1_2())
                    print(self.vels(speed,turn))
                    print('phase=2')
                    speed_msg = Float64()
                    turn_msg = Float64()
                    speed_msg.data = speed
                    turn_msg.data = turn
            
                    self.main_turn_pub.publish(turn_msg)
                    self.main_speed_pub.publish(speed_msg)

                else :
                    speed=0.0
                    turn=0.0
                    print('STOP')
                    speed_msg = Float64()
                    turn_msg = Float64()
                    speed_msg.data = speed
                    turn_msg.data = turn
            
                    self.main_turn_pub.publish(turn_msg)
                    self.main_speed_pub.publish(speed_msg)


            # speed=float(self.mot())
            # turn=float(self.dir())
            # print(self.vels(speed,turn))

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