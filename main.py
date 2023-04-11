#!/usr/bin/env pybricks-micropython
# from funcs.py import *

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.
 
# ----------------------------------------
# Constants
# ----------------------------------------
INIT_COLOR_REFLECTION_THRESHOLD = 10

# Speed constant
LOW_SPEED = 30
MEDIUM_SPEED = 45
HIGH_SPEED = 60
VERY_HIGH_SPEED = 80

# Port constants
TOUCH_SENSOR_PORT = Port.S1
COLOR_SENSOR_PORT = Port.S2
CLAW_MOTOR_PORT = Port.A
CRANE_MOTOR_PORT = Port.B
ROTATION_MOTOR_PORT = Port.C

# Gear constants
CRANE_BIG_GEAR_TOOTHCOUNT = 40
CRANE_SMALL_GEAR_TOOTHCOUNT = 8
CRANE_GEAR_RATIO = CRANE_BIG_GEAR_TOOTHCOUNT / CRANE_SMALL_GEAR_TOOTHCOUNT

ROTATION_BIG_GEAR_TOOTHCOUNT = 36
ROTATION_SMALL_GEAR_TOOTHCOUNT = 12
ROTATION_GEAR_RATIO = ROTATION_BIG_GEAR_TOOTHCOUNT / ROTATION_SMALL_GEAR_TOOTHCOUNT

# Angle constants
COLOR_TO_FLOOR_ANGLE = 30 * CRANE_GEAR_RATIO
CLAW_HEIGHT_IN_DEGREES_OF_CRANE_ROTATION = 13

CLAW_OPEN_ANGLE = 55
CLAW_CLOSED_ANGLE = 0

MAX_ROTATION_ANGLE = 190
MIN_ROTATION_ANGLE = -32

# Color constants
BASE_ANGLE = 190
COLOR_DICTIONARY = {
    Color.BLACK: 0,
    Color.BLUE:     BASE_ANGLE * 1 / 6,
    Color.GREEN:    BASE_ANGLE * 2 / 6,
    Color.YELLOW:   BASE_ANGLE * 3 / 6,
    Color.RED:      BASE_ANGLE * 4 / 6,
    Color.WHITE:    BASE_ANGLE * 5 / 6,
    Color.BROWN:    BASE_ANGLE * 6 / 6,
    None:          -BASE_ANGLE * 1 / 6,
}

# Duty
MAX_DUTY = 100

# ----------------------------------------
# Objects
# ----------------------------------------

ev3 = EV3Brick()
touchSensor = TouchSensor(TOUCH_SENSOR_PORT)
colorSensor = ColorSensor(COLOR_SENSOR_PORT)
clawMotor = Motor(CLAW_MOTOR_PORT)
craneMotor = Motor(CRANE_MOTOR_PORT)
rotationMotor = Motor(ROTATION_MOTOR_PORT)

craneMotor.control.limits(speed=VERY_HIGH_SPEED, acceleration=120)
rotationMotor.control.limits(speed=VERY_HIGH_SPEED, acceleration=120)

# ----------------------------------------
# Code
# ----------------------------------------


def init_claw_motor():
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / 4)

    clawMotor.reset_angle(CLAW_CLOSED_ANGLE)
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)


def init_crane_motor():
    craneMotor.run_time(-HIGH_SPEED, 3500)
    craneMotor.run(LOW_SPEED)

    while colorSensor.reflection() < INIT_COLOR_REFLECTION_THRESHOLD:
        wait(2)
    craneMotor.reset_angle(CLAW_HEIGHT_IN_DEGREES_OF_CRANE_ROTATION * CRANE_GEAR_RATIO)
    craneMotor.run_target(MEDIUM_SPEED, 0)


def init_rotation_motor():
    rotationMotor.reset_angle(0)


def init():
    init_claw_motor()
    init_crane_motor()
    init_rotation_motor()


def pick_item():
    initialAngle = craneMotor.angle()
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE, wait=False)
    craneMotor.run_until_stalled(HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO)
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.HOLD, duty_limit=MAX_DUTY / 2)
    craneMotor.run_target(LOW_SPEED, initialAngle)


def drop_item():
    initialAngle = craneMotor.angle()
    craneMotor.run_until_stalled(HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO)
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)
    craneMotor.run_target(LOW_SPEED, initialAngle)


def get_color():
    return colorSensor.color()


def get_color_rgb():
    return colorSensor.rgb()


def do_at(angle, func):
    if angle > MAX_ROTATION_ANGLE or angle < MIN_ROTATION_ANGLE:
        return
    initialAngle = rotationMotor.angle()
    rotationMotor.run_target(HIGH_SPEED, -ROTATION_GEAR_RATIO * angle)
    func()
    rotationMotor.run_target(HIGH_SPEED, ROTATION_GEAR_RATIO * initialAngle)


def drop_item_at(angle):
    do_at(angle, drop_item)


def pick_item_at(angle):
    do_at(angle, pick_item)


def drop_item_by_color(color_dictionary=COLOR_DICTIONARY):
    color = get_color()
    angle = color_dictionary[color]
    drop_item_at(angle)


def user_generate_color_dictionary():
    print(
"""
Select one of the colors:
Black, Blue, Green, Yellow, Red, White, Brown.
For each position...\
"""
    )
    STRING_TO_COLOR_DICTIONARY = {"black":Color.BLACK,"blue":Color.BLUE,"green":Color.GREEN,"yellow":Color.YELLOW,"red":Color.RED,"white":Color.WHITE,"brown":Color.BROWN}
    color_dictionary = dict()
    for i in range(3):
        print()
        color = input("Select color for position " + str(i+1) + ": ").lower()
        angle = float(input("Select angle for position " + str(i+1) + ": "))
        color_dictionary[STRING_TO_COLOR_DICTIONARY[color]] = angle
    return color_dictionary


def main():
    init()
    pick_item()
    drop_item_at(90)
    pick_item_at(90)
    while True:
        craneMotor.hold()


main()
