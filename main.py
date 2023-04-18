#!/usr/bin/env pybricks-micropython
# from funcs.py import *
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# ----------------------------------------
# Constants
# ----------------------------------------
INIT_COLOR_REFLECTION_THRESHOLD = 12

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

# Color dictionary function
MIN_NUMBER_POSITIONS = 3
STRING_TO_COLOR_DICTIONARY = {"black":Color.BLACK,"blue":Color.BLUE,"green":Color.GREEN,"yellow":Color.YELLOW,"red":Color.RED,"white":Color.WHITE,"brown":Color.BROWN}

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
    craneMotor.run_time(-VERY_HIGH_SPEED, 3000)
    craneMotor.run(HIGH_SPEED)

    while colorSensor.reflection() < INIT_COLOR_REFLECTION_THRESHOLD:
        wait(2)
    craneMotor.reset_angle(CLAW_HEIGHT_IN_DEGREES_OF_CRANE_ROTATION * CRANE_GEAR_RATIO)
    craneMotor.run_target(HIGH_SPEED, 0)


def init_rotation_motor():
    rotationMotor.run(MEDIUM_SPEED)
    while not touchSensor.pressed():
        wait(2)
    rotationMotor.stop()
    rotationMotor.reset_angle(0)


def init():
    init_claw_motor()
    init_crane_motor()
    init_rotation_motor()


def pick_item():
    initialAngle = craneMotor.angle()
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE, wait=False)
    craneMotor.run_until_stalled(HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO)
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.HOLD, duty_limit=MAX_DUTY * .8)
    craneMotor.run_target(HIGH_SPEED, initialAngle)


def drop_item():
    initialAngle = craneMotor.angle()
    craneMotor.run_until_stalled(HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO)
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)
    craneMotor.run_target(HIGH_SPEED, initialAngle)


def get_color():
    return colorSensor.color()


def get_color_rgb():
    return colorSensor.rgb()


def do_at(angle, func):
    if angle > MAX_ROTATION_ANGLE or angle < MIN_ROTATION_ANGLE:
        raise ValueError("Use angle in range [0, 190].")
    else:
        initialAngle = rotationMotor.angle()
        rotationMotor.run_target(VERY_HIGH_SPEED, -ROTATION_GEAR_RATIO * angle)
        return_value = func()
        rotationMotor.run_target(VERY_HIGH_SPEED, ROTATION_GEAR_RATIO * initialAngle)
        return return_value


def drop_item_at(angle):
    do_at(angle, drop_item)


def pick_item_at(angle):
    do_at(angle, pick_item)


def drop_item_by_color(color, color_dictionary=COLOR_DICTIONARY):
    try:
        angle = color_dictionary[color]
    except (KeyError, ValueError) as error:
        print(error)
        print("No such color in color_dictionary.")
    else:
        drop_item_at(angle)


def user_generate_color_dictionary():
    print(
"""
Select one of the colors:
Black, Blue, Green, Yellow, Red, White, Brown.
Select an angle in [0, 180].
Select number of positions (minimum 3).
For each position...\
"""
    )
    rotationMotor.stop()

    color_dictionary = dict()

    positions_input_lambda = lambda: int(input("Select number of positions: "))
    color_input_lambda = lambda: input("Select color for position " + str(i+1) + ": ").lower()

    positions = positions_input_lambda()
    while positions < MIN_NUMBER_POSITIONS:
        print("Please enter an integer greater or equal to", MIN_NUMBER_POSITIONS)
        positions = positions_input_lambda()

    for i in range(positions):
        print("\nPosition ", str(i+1), ":", sep='')

        color = color_input_lambda()
        while color not in STRING_TO_COLOR_DICTIONARY.keys():
            print("Please enter a color in", str(STRING_TO_COLOR_DICTIONARY.keys()))
            color = color_input_lambda()

        input("Press enter to select current position as drop-off zone.")
        angle = -rotationMotor.angle() / ROTATION_GEAR_RATIO

        color_dictionary[STRING_TO_COLOR_DICTIONARY[color]] = angle
    return color_dictionary


def hold():
    wait(5000)


def check_item():
    """Return True if item present at current location, otherwise False."""
    initialAngle = craneMotor.angle()
    craneMotor.run_until_stalled(HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO)
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.HOLD, duty_limit=MAX_DUTY / 2)
    claw_angle = clawMotor.angle()
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)
    craneMotor.run_target(HIGH_SPEED, initialAngle)
    return claw_angle > 2


def check_item_at(angle):
    return do_at(angle, check_item)


def get_color_at(angle):
    pick_item_at(angle)
    color = get_color()
    drop_item_at(angle)
    return color


def check_periodically_at(period, angle):
    """Check if item at designated angle at every period (ms)."""
    while not check_item_at(angle):
        wait(period)


def configure_sorting_locations():
    """US12"""
    initial_angle = rotationMotor.angle()
    rotationMotor.stop()
    input("Press enter to select current position as pick-up zone.")
    number_of_drop_off_zones = int(input("Enter number of drop-off zones to configure: "))
    pick_up_zone = -rotationMotor.angle() / ROTATION_GEAR_RATIO
    drop_off_zones = []
    for i in range(1, number_of_drop_off_zones+1):
        input("Press enter to select current position as drop-off zone " + str(i) + ".")
        drop_off_zones.append(-rotationMotor.angle() / ROTATION_GEAR_RATIO)
    rotationMotor.run_target(HIGH_SPEED, initial_angle)
    return pick_up_zone, drop_off_zones



def sort(color_dictionary):
    pick_item_at(0)
    color = get_color()
    if color not in color_dictionary:
        return False
    drop_item_at(color_dictionary[color])
    return True


if __name__ == "__main__":
    init()
    craneMotor.stop()
    input()
    print(craneMotor.angle())
