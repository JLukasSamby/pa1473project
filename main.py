#!/usr/bin/env pybricks-micropython
from funcs.py import *

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

# Port constants
TOUCH_SENSOR_PORT = Port.S1
COLOR_SENSOR_PORT = Port.S2
CLAW_MOTOR_PORT = Port.A
CRANE_MOTOR_PORT = Port.B
ROTATION_MOTOR_PORT = Port.C

# Gear constants
BIG_GEAR_TOOTHCOUNT = 40
SMALL_GEAR_TOOTHCOUNT = 8
CRANE_GEAR_RATIO = BIG_GEAR_TOOTHCOUNT / SMALL_GEAR_TOOTHCOUNT

# ----------------------------------------
# Objects
# ----------------------------------------
ev3 = EV3Brick()
touchSensor = TouchSensor(TOUCH_SENSOR_PORT)
colorSensor = ColorSensor(COLOR_SENSOR_PORT)
clawMotor = Motor(CLAW_MOTOR_PORT)
craneMotor = Motor(CRANE_MOTOR_PORT)
rotationMotor = Motor(ROTATION_MOTOR_PORT)

craneMotor.control.limits(speed=60, acceleration=120)
rotationMotor.control.limits(speed=60, acceleration=120)

# ----------------------------------------
# Code
# ----------------------------------------


def init():
    craneMotor.run_time(-60, 3000)
    craneMotor.run(20)

    while colorSensor.reflection() < 15:
        print(colorSensor.reflection())
        wait(10)
    craneMotor.reset_angle(12 * CRANE_GEAR_RATIO)
    craneMotor.run_target(45, 0)


def main():
    init()
    while True:
        craneMotor.hold()


main()
