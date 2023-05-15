#!/usr/bin/env pybricks-micropython
from constants import (
    CLAW_CLOSED_ANGLE, 
    CLAW_OPEN_ANGLE,
    LOW_SPEED,MAX_DUTY,
    HIGH_SPEED,
    MEDIUM_SPEED,
    CRANE_GEAR_RATIO,
    CLAW_HEIGHT_IN_DEGREES_OF_CRANE_ROTATION,
    INIT_COLOR_REFLECTION_THRESHOLD,
    VERY_HIGH_SPEED
)
from robot_setup import(
    clawMotor,
    craneMotor,
    rotationMotor,
    colorSensor,
    touchSensor
)
from pybricks.parameters import Stop
from io import notify
from core import hold


def init_claw_motor(verbose=False):
    """
    Initialize the claw motor.

    After initialization the reset angle (0) of the claw motor is
    when the claw is closed.

    Parameters:
        verbose (bool): If to notify the user of initialization. Default False.
    """
    if verbose:
        notify("Calibraint claw.")

    clawMotor.run_until_stalled(-LOW_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY)
    clawMotor.reset_angle(CLAW_CLOSED_ANGLE)
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)


def init_crane_motor(verbose=False):
    """
    Initialize the crane motor.

    After initialization the reset angle (0) of the crane motor is at the position
    where a held brick will be at the height of the color sensor.

    Parameters:
        verbose (bool): If to notify the user of initialization. Default False.
    """
    if verbose:
        notify("Calibrati crane.")
    craneMotor.run_time(-VERY_HIGH_SPEED, 4000)
    craneMotor.run(HIGH_SPEED)

    while colorSensor.reflection() < INIT_COLOR_REFLECTION_THRESHOLD:
        hold(2)
    craneMotor.reset_angle(CLAW_HEIGHT_IN_DEGREES_OF_CRANE_ROTATION * CRANE_GEAR_RATIO)
    craneMotor.run_target(HIGH_SPEED, 0)


def init_rotation_motor(verbose=False):
    """
    Initialize the rotation motor.

    After initialization the reset angle (0) of the rotation motor is at the
    default drop off zone, when the robot pushes the pushbutton at rotation
    base.

    Parameters:
        verbose (bool): If to notify the user of initialization. Default False.
    """
    if verbose:
        notify("Calibrating rotation.")

    rotationMotor.run(MEDIUM_SPEED)
    while not touchSensor.pressed():
        hold(2)
    rotationMotor.reset_angle(-3)
    rotationMotor.stop()
    rotationMotor.run_target(HIGH_SPEED, 0)


def init(verbose=False):
    """
    Initialize the robots motors.

    Parameters:
        verbose (bool): If to notify the user of initialization. Default False.
    """
    if verbose:
        notify("Initializing...")
    init_rotation_motor(verbose=verbose)
    init_claw_motor(verbose=verbose)
    init_crane_motor(verbose=verbose)
