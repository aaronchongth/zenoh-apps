#!/usr/bin/python3

import time
import pickle
import argparse

from Messages import Time, Location, RobotMode, RobotState

from zenoh.net import Session, SubscriberMode


def listener(rname, data, info):
    state_msg = pickle.loads(data)
    print(state_msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Server',
        description='Server that listens to RobotState over zenoh')
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
    sub = s.declare_subscriber(args.path, SubscriberMode.push(), listener)

    while True:
        print('Server is running...')
        time.sleep(10.0)

    s.undeclare_subscriber(sub)
    s.close()
