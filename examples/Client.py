#!/usr/bin/python3

import time
import pickle
import argparse

from Messages import Time, Location, RobotMode, RobotState

from zenoh.net import Session

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Client',
        description='Client that publishes RobotState over zenoh')
    parser.add_argument(
        '--name', '-n', dest='name',
        default='client',
        type=str,
        help='The name of the client used as an identifier.')
    parser.add_argument(
        '--locator', '-l', dest='locator',
        default=None,
        type=str,
        help='The locator too be used to bootstrap the zenoh session.'
            ' By default dynamic discovery is used.')
    parser.add_argument(
        '--path', '-p', dest='path',
        default='/zenoh/robot_states',
        type=str,
        help='The resource used to write state data')
    args = parser.parse_args()

    s = Session.open(args.locator)
    pub = s.declare_publisher(args.path)

    current_time = Time(sec=0, nanosec=0)
    test_location = Location(
        t=current_time, 
        x=123.123, 
        y=234.234, 
        yaw=345.345,
        level_name='test_location')
    test_mode = RobotMode(mode=RobotMode.MODE_IDLE)
    current_state = RobotState(
        name=args.name,
        model='test_robot_model',
        task_id='',
        mode=test_mode,
        battery_percent=0.0,
        location=test_location,
        path=[test_location, test_location, test_location])

    curr_iter = 0
    while True:
        current_state.location.t.sec = curr_iter

        serialized_state = pickle.dumps(current_state)
        print('Sending a message of iteration: {}'.format(curr_iter))
        s.stream_data(pub, serialized_state)

        curr_iter += 1
        time.sleep(1.0)

    s.close()
