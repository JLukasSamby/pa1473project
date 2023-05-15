#!/usr/bin/env pybricks-micropython
from pybricks.tools import wait
from pick import pick_stalled, pick_height
from drop import drop_stalled, drop_height
from constants import (
    MAX_ROTATION_ANGLE,
    MIN_ROTATION_ANGLE,
    HIGH_SPEED,
    CRANE_GEAR_RATIO,
    CRANE_RESTING_HIGH_ANGLE,
    VERY_HIGH_SPEED,
    ROTATION_GEAR_RATIO,
    CLAW_CLOSED_ANGLE,
    CLAW_OPEN_ANGLE,
    COLOR_DICTIONARY
)
from robot_setup import (
    craneMotor,
    rotationMotor,
    clawMotor,
    colorSensor
)
from io import notify


def do_at(angle: float, func: "Callable", *args: "tuple", should_return=True) -> any:
    """
    Rotate to given angle and perform the function with given args. 

    Parameters:
        angle (float): angle to drop at
        func (Callable(...)): callable which parameters match that of *args
        args (tuple): tuple containing the arguments to be unpacked when calling func
        should_return (bool): if the initial position should be returned to after rotation
                              and executing func. Default True.
    """
    if angle > MAX_ROTATION_ANGLE or angle < MIN_ROTATION_ANGLE:
        raise ValueError("Use angle in range [0, 190].")

    if should_return:
        initial_rotation_angle = rotationMotor.angle()
        initial_crane_angle = craneMotor.angle()

    craneMotor.run_target(HIGH_SPEED, -CRANE_GEAR_RATIO * CRANE_RESTING_HIGH_ANGLE)
    rotationMotor.run_target(VERY_HIGH_SPEED, -ROTATION_GEAR_RATIO * angle)
    if len(args) > 0:
        return_value = func(*args)
    else:
        return_value = func()

    if should_return:
        craneMotor.run_target(VERY_HIGH_SPEED, -CRANE_GEAR_RATIO * CRANE_RESTING_HIGH_ANGLE)
        rotationMotor.run_target(VERY_HIGH_SPEED, ROTATION_GEAR_RATIO * initial_rotation_angle)
        craneMotor.run_target(HIGH_SPEED, CRANE_GEAR_RATIO * initial_crane_angle)
    return return_value


def pick(angle: float=None, height: float=None, should_return: bool=True):
    """
    Drop currently held item at given angle and height; potentially return.

    Angle and height are both optional, omitting angle will default
    to current rotation position and omitting height will default to
    floor height.

    Parameters:
        angle (float): the rotation angle to check
        height (float): the height to check (given in degrees of crane rotation)
        shold_return (bool): if the initial position should be returned to after drop.
                             Default True.

    Returns:
        Rgb: the current rgb values read from sensor
    """
    if angle is None and height is None:
        pick_stalled()
    elif height is None:
        do_at(angle, pick_stalled, should_return=should_return)
    elif angle is None:
        pick_height(height)
    else:
        do_at(angle, pick_height, height, should_return=should_return)


def drop(
    angle: float = None,
    height: float = None,
    should_return: bool = True
) -> None:
    """
    Drop currently held item at given angle and height; potentially return.

    Angle and height are both optional, omitting angle will default
    to current rotation position and omitting height will default to
    floor height.

    Parameters:
        angle (float): the rotation angle to check. Default None.
        height (float): the height to check (given in degrees of crane rotation). Default
                        None.
        shold_return (bool): if the initial position should be returned to after drop.
                             Default True.

    Returns:
        Rgb: the current rgb values read from sensor
    """
    if angle is None and height is None:
        drop_stalled()
    elif height is None:
        do_at(angle, drop_stalled, should_return=should_return)
    elif angle is None:
        drop_height(height)
    else:
        do_at(angle, drop_height, height, should_return=should_return)



def item_in_place(angle: float=None, height: float=None) -> bool:
    """
    Return if item precent at given angle and height.

    Angle and height are both optional, omitting angle will default
    to current rotation position and omitting height will default to
    floor height.

    Parameters:
        angle (float): the rotation angle to check. Default None.
        height (float): the height to check (given in degrees of crane rotation).
                        Default None.

    Returns:
        bool: if there is an item present
    """
    pick(angle=angle, height=height)
    claw_angle = clawMotor.angle()
    notify(str(claw_angle))
    condition = claw_angle < CLAW_CLOSED_ANGLE + 10
    if condition:
        drop(angle=angle, height=height)
    else:
        clawMotor.run_target(VERY_HIGH_SPEED, CLAW_OPEN_ANGLE)
    return condition


def drop_item_by_color(color: "Color", color_dictionary: dict=COLOR_DICTIONARY) -> None:
    """
    Perform drop at the location corresponding to given color in color_dictionary.

    Parameters:
        color (Color): the color of the brick
        color_dictionary (dict): the dictionary with positions for different colors.
                                 Default COLOR_DICTIONARY, see constants.py.
    """
    try:
        angle = color_dictionary[color]
    except (KeyError, ValueError) as error:
        print(error)
        print("No such color in color_dictionary.")
    else:
        drop(angle=angle)


def get_color() -> "Color":
    """
    Return closest color read from color sensor.

    Returns:
        Color: The current color value read from sensor
    """
    return colorSensor.color()


def get_color_rgb() -> tuple(int, int, int):
    """
    Return closest rbg value from color sensor

    Returns:
        tuple(int, int, int): the current rgb values read from sensor
    """
    return colorSensor.rgb()


def hold(time=5000):
    """
    Wait in a set time if not sent a diffrent time
    Parameters:
            time(int):wait in 5 secends if no parameter get send else wait of the sent value
    
    """
    wait(time)
