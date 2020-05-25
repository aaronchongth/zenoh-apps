#!/usr/bin/python3

import pickle
from typing import List
from recordclass import RecordClass


class Time(RecordClass):
    sec: int
    nanosec: int


class RobotMode(RecordClass):
    mode: int
    
    MODE_IDLE = 0
    MODE_CHARGING = 1
    MODE_MOVING = 2
    MODE_PAUSED = 3
    MODE_WAITING = 4
    MODE_EMERGENCY = 5
    MODE_GOING_HOME = 6
    MODE_DOCKING = 7


class Location(RecordClass):
    t: Time
    x: float
    y: float
    yaw: float
    level_name: str


class RobotState(RecordClass):
    name: str
    model: str
    task_id: str
    mode: RobotMode
    battery_percent: float
    location: Location
    path: List[Location]


# if __name__ == '__main__':
#     test_time = Time(sec=10, nanosec=12)
#     test_location = Location(
#         t=test_time, 
#         x=123.123, 
#         y=234.234, 
#         yaw=345.345,
#         level_name='test_location')
#     test_mode = RobotMode(mode=RobotMode.MODE_IDLE)
#     test_state = RobotState(
#         name='test_robot',
#         model='test_robot_model',
#         task_id='test_robot_task_id',
#         mode=test_mode,
#         battery_percent=123.123,
#         location=test_location,
#         path=[test_location, test_location, test_location])

#     serialized_state = pickle.dumps(test_state)
#     print(len(serialized_state))
#     deserialized_state = pickle.loads(serialized_state)
#     print(deserialized_state)
