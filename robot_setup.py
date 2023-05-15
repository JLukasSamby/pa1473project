#!/usr/bin/env pybricks-micropython
from constants import (
    COLOR_SENSOR_PORT,
    CLAW_MOTOR_PORT,
    CRANE_MOTOR_PORT,
    ROTATION_MOTOR_PORT,
    TOUCH_SENSOR_PORT,
    VERY_HIGH_SPEED
)
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor
)

ev3 = EV3Brick()
touchSensor = TouchSensor(TOUCH_SENSOR_PORT)
colorSensor = ColorSensor(COLOR_SENSOR_PORT)
clawMotor = Motor(CLAW_MOTOR_PORT)
craneMotor = Motor(CRANE_MOTOR_PORT)
rotationMotor = Motor(ROTATION_MOTOR_PORT)
screen = ev3.screen
speaker = ev3.speaker
buttons = ev3.buttons

craneMotor.control.limits(speed=VERY_HIGH_SPEED, acceleration=120)
rotationMotor.control.limits(speed=VERY_HIGH_SPEED, acceleration=120)
