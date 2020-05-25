#!/usr/bin/python3

import argparse

from Messages import *

import tf
import rospy
import actionlib
from std_msgs.msg import String
from sensor_msgs.msg import BatteryState
from geometry_msgs.msg import Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

from zenoh.net import Session


class ClientNode:
    def __init__(self, args):
        print('ClientNode starting...')
        self.robot_name = args.robot_name
        self.robot_model = args.robot_model
        self.battery_state_topic = args.battery_state_topic
        self.level_name_topic = args.level_name_topic
        self.map_frame = args.map_frame
        self.robot_frame = args.robot_frame
        self.move_base_server = args.move_base_server

        self.tf_listener = tf.TransformListener()
        rospy.Subscriber(
                args.battery_state_topic, BatteryState, self.update_battery_cb)
        self.move_base_client = actionlib.SimpleActionClient(
                self.move_base_server_name, MoveBaseAction)

        max_attempts = 10
        curr_attempt = 0
        while not self.move_base_client.wait_for_server(timeout=rospy.Duration(1.0))


    def update_battery_cb(self, msg):
        raise NotImplementedError
    

    def send_robot_state(self):
        curr_robot_state = RobotState()
        curr_robot_state.robot_time = rospy.Time.now()
        curr_robot_state.robot_name = self.robot_name
        curr_robot_state.status = self.robot_status
        curr_robot_state.location = self.robot_current_location
        curr_robot_state.task_queue.append(self.robot_current_task)
        curr_robot_state.battery_percent = self.robot_battery
        curr_robot_state.mode = self.robot_mode
        packet = self.robot_state_parser.msg_to_packet(curr_robot_state)
        self.robot_socket.sendto(packet.bytes, self.fm_address)


    def update_pose(self):
        try:
            (trans, rot) = self.tf_listener.lookupTransform(
                    '/map', '/base_footprint', rospy.Time(0))
            robot_position = Point()
            robot_position.x = trans[0]
            robot_position.y = trans[1]
            robot_position.z = trans[2]
            robot_twist = Quaternion()
            robot_twist.x = rot[0]
            robot_twist.y = rot[1]
            robot_twist.z = rot[2]
            robot_twist.w = rot[3]
            self.robot_current_location.position = robot_position
            self.robot_current_location.orientation = robot_twist
            self.robot_status = 'operational'
        except (tf.LookupException, tf.ConnectivityException, 
                tf.ExtrapolationException):
            self.robot_status = 'localization lost'


    def main(self):
        while not rospy.is_shutdown():
            self.update_pose()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    argv = rospy.myargv()
    args = parser.parse_args(argv[1:])
    
    rospy.init_node('zenoh_client_node', anonymous=True)
    client_node = ClientNode(args)
    client_node.main()
