#!/usr/bin/env pybricks-micropython
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
TOUCH_SENSOR_PORT = 0
COLOR_SENSOR_PORT = 0

# Create your objects here.
ev3 = EV3Brick()
touchSensor = Motor(TOUCH_SENSOR_PORT)
colorSensor = Motor(COLOR_SENSOR_PORT)

# Write your program here.
ev3.speaker.beep()
