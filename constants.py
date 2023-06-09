#!/usr/bin/env pybricks-micropython
"""
This file containts a collection of constants that are used across all functoions.
They are gathered here to reduce cognitive load instead and reduce clutter.
"""

from pybricks.parameters import Color, Port


INIT_COLOR_REFLECTION_THRESHOLD = 12

# Speed constant
LOW_SPEED = 30
MEDIUM_SPEED = 45
HIGH_SPEED = 80
VERY_HIGH_SPEED = 120

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
CRANE_RESTING_HIGH_ANGLE = 40

COLOR_TO_FLOOR_ANGLE = 30 * CRANE_GEAR_RATIO
CLAW_HEIGHT_IN_DEGREES_OF_CRANE_ROTATION = 13

CLAW_OPEN_ANGLE = 90
CLAW_CLOSED_ANGLE = 0

MAX_ROTATION_ANGLE = 210
MIN_ROTATION_ANGLE = -30

# Color constants
BASE_ANGLE = 190
COLOR_DICTIONARY = {
    Color.BLACK: 0,
    Color.BLUE: BASE_ANGLE * 1 / 6,
    Color.GREEN: BASE_ANGLE * 2 / 6,
    Color.YELLOW: BASE_ANGLE * 3 / 6,
    Color.RED: BASE_ANGLE * 4 / 6,
    Color.WHITE: BASE_ANGLE * 5 / 6,
    Color.BROWN: BASE_ANGLE * 6 / 6,
    None: -BASE_ANGLE * 1 / 6,
}

# Duty
MAX_DUTY = 100

# Configuration time constants
CHECK_INTERVAL_IN_MILLISECONDS = 10

# Color dictionary function
MIN_NUMBER_POSITIONS = 3
STRING_TO_COLOR_DICTIONARY = {
    "black": Color.BLACK,
    "blue": Color.BLUE,
    "green": Color.GREEN,
    "yellow": Color.YELLOW,
    "red": Color.RED,
    "white": Color.WHITE,
    "brown": Color.BROWN,
}
