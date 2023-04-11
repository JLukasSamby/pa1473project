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
COLOR_ZERO = 10

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

# Color constants
BASE_ANGLE = 190
COLOR_DICTIONARY = {
    Color.BLACK: 0,
    Color.BLUE:     BASE_ANGLE * 1 / 6,
    Color.GREEN:    BASE_ANGLE * 2 / 6,
    Color.YELLOW:   BASE_ANGLE * 3 / 6,
    Color.RED:      BASE_ANGLE * 4 / 6, ##test
    Color.WHITE:    BASE_ANGLE * 5 / 6,
    Color.BROWN:    BASE_ANGLE * 6 / 6,
    None:          -BASE_ANGLE * 1 / 6,
}

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


def init():
    # Initialize claw motor
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.COAST, duty_limit=25)

    clawMotor.reset_angle(0)
    clawMotor.run_target(HIGH_SPEED, 55)

    # Initialize crane motor
    craneMotor.run_time(-HIGH_SPEED, 3500)
    craneMotor.run(LOW_SPEED)

    while colorSensor.reflection() < COLOR_ZERO:
        print(colorSensor.reflection())
        wait(5)
    craneMotor.reset_angle(12 * CRANE_GEAR_RATIO)
    craneMotor.run_target(MEDIUM_SPEED, 0)

    # Initialize rotation motor
    rotationMotor.reset_angle(0)


def pick_item():
    initialAngle = craneMotor.angle()
    clawMotor.run_target(HIGH_SPEED, 55, wait=False)
    craneMotor.run_until_stalled(HIGH_SPEED, then=Stop.COAST, duty_limit=100 / CRANE_GEAR_RATIO)
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.HOLD, duty_limit=50)
    craneMotor.run_target(LOW_SPEED, initialAngle)


def drop_item():
    initialAngle = craneMotor.angle()
    craneMotor.run_until_stalled(HIGH_SPEED, then=Stop.COAST, duty_limit=100 / CRANE_GEAR_RATIO)
    clawMotor.run_target(HIGH_SPEED, 55)
    craneMotor.run_target(LOW_SPEED, initialAngle)


def get_color():
    return colorSensor.color()


# REfactor to use a "do_at" function taking a function and an angle. To remove duplicated code

def drop_item_at(angle):
    initialAngle = rotationMotor.angle()
    rotationMotor.run_target(HIGH_SPEED, -ROTATION_GEAR_RATIO * angle)
    drop_item()
    rotationMotor.run_target(HIGH_SPEED, ROTATION_GEAR_RATIO * initialAngle)


def pick_item_at(angle):
    initialAngle = rotationMotor.angle()
    rotationMotor.run_target(HIGH_SPEED, ROTATION_GEAR_RATIO * angle)
    drop_item()
    rotationMotor.run_target(HIGH_SPEED, ROTATION_GEAR_RATIO * initialAngle)


def drop_item_by_color():
    pick_item()
    color = get_color()
    angle = COLOR_DICTIONARY[color]
    drop_item_at(angle)


def main():
    init()
    drop_item_by_color()
    while True:
        craneMotor.hold()


main()
