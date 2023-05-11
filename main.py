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

# ----------------------------------------
# Constants
# ----------------------------------------
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


def init_claw_motor(verbose=False):
    if verbose:
        print("Stage 1. Calibrating the claw")
        ev3.speaker.beep(frequency=500, duration=100)
    clawMotor.run_until_stalled(-LOW_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY)
    clawMotor.reset_angle(CLAW_CLOSED_ANGLE)
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)


def init_crane_motor(verbose=False):
    if verbose:
        print("Stage 2. Calibrating the crane")
        for _ in range(2):
            ev3.speaker.beep(frequency=500, duration=200)
    craneMotor.run_time(-VERY_HIGH_SPEED, 4000)
    craneMotor.run(HIGH_SPEED)

    while colorSensor.reflection() < INIT_COLOR_REFLECTION_THRESHOLD:
        wait(2)
    craneMotor.reset_angle(CLAW_HEIGHT_IN_DEGREES_OF_CRANE_ROTATION * CRANE_GEAR_RATIO)
    craneMotor.run_target(HIGH_SPEED, 0)


def init_rotation_motor(verbose=False):
    if verbose:
        print("Stage 3. Calibrating the rotation motor")
        for _ in range(3):
            ev3.speaker.beep(frequency=500, duration=100)
        
    rotationMotor.run(MEDIUM_SPEED)
    while not touchSensor.pressed():
        wait(2)
    rotationMotor.reset_angle(0)
    rotationMotor.stop()
    rotationMotor.run_target(HIGH_SPEED, 0)


def init(verbose=False):
    ev3.speaker.say(“Resetting”)
    init_rotation_motor(verbose=verbose)
    init_claw_motor(verbose=verbose)
    init_crane_motor(verbose=verbose)


def pick_item():
    initialAngle = craneMotor.angle()
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE, wait=False)
    craneMotor.run_until_stalled(
        HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO
    )
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.HOLD, duty_limit=MAX_DUTY * 0.8)
    craneMotor.run_target(HIGH_SPEED, initialAngle)


def drop_item():
    initialAngle = craneMotor.angle()
    craneMotor.run_until_stalled(
        HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO
    )
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)
    craneMotor.run_target(HIGH_SPEED, initialAngle)


def get_color():
    return colorSensor.color()


def get_color_rgb():
    return colorSensor.rgb()


def do_at(angle, func, *args):
    if angle > MAX_ROTATION_ANGLE or angle < MIN_ROTATION_ANGLE:
        raise ValueError("Use angle in range [0, 190].")

    initialRotationAngle = rotationMotor.angle()
    initialCraneAngle = craneMotor.angle()
    craneMotor.run_target(HIGH_SPEED, -CRANE_GEAR_RATIO * CRANE_RESTING_HIGH_ANGLE)
    rotationMotor.run_target(VERY_HIGH_SPEED, -ROTATION_GEAR_RATIO * angle)
    if len(args) > 0:
        return_value = func(*args)
    else:
        return_value = func()
    rotationMotor.run_target(VERY_HIGH_SPEED, ROTATION_GEAR_RATIO * initialRotationAngle)
    craneMotor.run_target(HIGH_SPEED, CRANE_GEAR_RATIO * initialCraneAngle)
    return return_value


def drop_item_at(angle):
    do_at(angle, drop_item)


def pick_item_at(angle):
    do_at(angle, pick_item)


def pick_item_height(height):
    initial_angle = craneMotor.angle()
    craneMotor.run_target(HIGH_SPEED, height)
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.HOLD, duty_limit=MAX_DUTY * 0.8)
    craneMotor.run_target(HIGH_SPEED, initial_angle)


def drop_item_height(height):
    initial_angle = craneMotor.angle()
    craneMotor.run_target(HIGH_SPEED, height)
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)
    craneMotor.run_target(HIGH_SPEED, initial_angle)


def pick_item_at_height(angle, height):
    do_at(angle, pick_item_height, height)


def drop_item_at_height(angle, height):
    do_at(angle, drop_item_height, height)


def drop_item_by_color(color, color_dictionary=COLOR_DICTIONARY):
    try:
        angle = color_dictionary[color]
    except (KeyError, ValueError) as error:
        print(error)
        print("No such color in color_dictionary.")
    else:
        drop_item_at(angle)


def user_generate_color_dictionary():
    print("""
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
    color_input_lambda = lambda: input(
        "Select color for position " + str(i + 1) + ": "
    ).lower()

    positions = positions_input_lambda()
    while positions < MIN_NUMBER_POSITIONS:
        print("Please enter an integer greater or equal to", MIN_NUMBER_POSITIONS)
        positions = positions_input_lambda()

    for i in range(positions):
        print("\nPosition ", str(i + 1), ":", sep="")

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
    craneMotor.run_until_stalled(
        HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO
    )
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
    while True:
        if check_item_at(angle):
            ev3.speaker.beep(frequency=500, duration=100)
        wait(period)


def sort_periodically_at(period, angle, color_dictionary=COLOR_DICTIONARY):
    """Check if item at designated angle at every period (ms)."""
    while True:
        sort(color_dictionary, angle)
        wait(period)


def configure_sorting_locations():
    """US12"""
    initial_angle = rotationMotor.angle()
    rotationMotor.stop()
    input("Press enter to select current position as pick-up zone.")
    number_of_drop_off_zones = int(
        input("Enter number of drop-off zones to configure: ")
    )
    pick_up_zone = -rotationMotor.angle() / ROTATION_GEAR_RATIO
    drop_off_zones = []
    for i in range(1, number_of_drop_off_zones + 1):
        input("Press enter to select current position as drop-off zone " + str(i) + ".")
        drop_off_zones.append(-rotationMotor.angle() / ROTATION_GEAR_RATIO)
    rotationMotor.run_target(HIGH_SPEED, initial_angle)
    return pick_up_zone, drop_off_zones


def sort(color_dictionary=COLOR_DICTIONARY, angle=0, include_heights=False):
    pick_item_at(angle)
    color = get_color()
    if color not in color_dictionary:
        drop_item_at(angle)
        return False
    if include_heights:
        drop_item_at_height(*color_dictionary[color])
    else:
        drop_item_at(color_dictionary[color])
    return True


def configure_height_and_angle_positions():
    initial_rotation = rotationMotor.angle()
    initial_crane_height = craneMotor.angle()
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)
    angle_rotation = angle_crane = None
    while True:
        pressed = ev3.buttons.pressed()

        if Button.CENTER in pressed:
            craneMotor.hold()
            rotationMotor.hold()
            angle_rotation = -rotationMotor.angle() / ROTATION_GEAR_RATIO
            angle_crane = craneMotor.angle()
            break

        if Button.UP in pressed:
            craneMotor.run(-MEDIUM_SPEED)
        elif Button.DOWN in pressed:
            craneMotor.run(MEDIUM_SPEED)
        else:
            craneMotor.hold()

        if Button.RIGHT in pressed and rotationMotor.angle() / ROTATION_GEAR_RATIO < MIN_ROTATION_ANGLE:
            rotationMotor.run(VERY_HIGH_SPEED)
        elif Button.LEFT in pressed and rotationMotor.angle() / ROTATION_GEAR_RATIO > -MAX_ROTATION_ANGLE:
            rotationMotor.run(-VERY_HIGH_SPEED)
        else:
            rotationMotor.hold()
        wait(CHECK_INTERVAL_IN_MILLISECONDS)

    craneMotor.run_target(HIGH_SPEED, -CRANE_GEAR_RATIO * CRANE_RESTING_HIGH_ANGLE)
    rotationMotor.run_target(VERY_HIGH_SPEED, initial_rotation)
    craneMotor.run_target(HIGH_SPEED, initial_crane_height)
    return angle_rotation, angle_crane


def reset_position():
    craneMotor.run_target(VERY_HIGH_SPEED, 0)
    rotationMotor.run_target(VERY_HIGH_SPEED, 0)


def configure_zones(number_of_zones, include_heights=False):
    lst = []
    ev3.screen.print("Configuring zones...")
    for i in range(number_of_zones):
        ev3.screen.print("\tzone: " + str(i))
        angle_rotation, angle_crane = configure_height_and_angle_positions()
        if include_heights:
            lst.append((angle_rotation, angle_crane))
        else:
            lst.append(angle_rotation)
    ev3.screen.print("DONE configuring zones")
    return lst


if __name__ == "__main__":
    init()
    rotation_angle, crane_angle = configure_height_and_angle_positions()
    reset_position()
    pick_item_at_height(rotation_angle, crane_angle)
