#!/usr/bin/env pybricks-micropython
from constants import(VERY_HIGH_SPEED,
                    MEDIUM_SPEED,HIGH_SPEED,ROTATION_GEAR_RATIO,
                    MIN_ROTATION_ANGLE,MAX_ROTATION_ANGLE,
                    CHECK_INTERVAL_IN_MILLISECONDS,
                    CRANE_GEAR_RATIO,
                    CRANE_RESTING_HIGH_ANGLE,
                    CLAW_OPEN_ANGLE,
                    STRING_TO_COLOR_DICTIONARY,
                    MIN_NUMBER_POSITIONS
                    )

from robot_setup import(rotationMotor,
                        craneMotor,
                        clawMotor,
                        screen,
                        speaker,
                        buttons)
from pybricks.parameters import Button
from pybricks.tools import wait


def notify(message: str) -> None:
    """
    Notify user through terminal, screen and speaker.
    
    Parameters:
      message (str): message to notify user with.
    """
    print(message)
    screen.print(message)
    speaker.say(message)


def configure_height_and_angle_positions() -> tuple:
    """
    Configure a specific zone by pressing buttons on the robot. 

    Use buttons on the ev3 to change height and move left and right. Center button to commit position.

    Returns:
      tuple(angle (float), height (float)): angle and height of commited positions
    """
    initial_rotation = rotationMotor.angle()
    initial_crane_height = craneMotor.angle()
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)
    angle_rotation = angle_crane = None
    while True:
        pressed = buttons.pressed()

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


def configure_zones(number_of_zones, include_heights=False):
    """
    Configure some number of zones using the buttons.

    Use buttons on the ev3 to change height and move left and right. Center button to commit position.

    Parameters:
      number_of_zones (int): number of zones to configure
      include_heights (bool): Whether to include the heights in the list. Default False.

    Returns:
      if include_heights:
        lst[tuple(angle (float), height (float))]: list of tuples of angle and height of commited positions.
      else:
        lst[float]: list of angles
    """
    lst = []
    notify("Configuring zones")

    for i in range(number_of_zones):
        ev3.screen.print("\tzone: " + str(i))
        angle_rotation, angle_crane = configure_height_and_angle_positions()
        if include_heights:
            lst.append((angle_rotation, angle_crane))
        else:
            lst.append(angle_rotation)
    notify("DONE configuring zones")
    return lst


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
        while color not in STRING_TO_COLOR_DICTIONARY:
            print("Please enter a color in", str(STRING_TO_COLOR_DICTIONARY.keys()))
            color = color_input_lambda()

        input("Press enter to select current position as drop-off zone.")
        angle = -rotationMotor.angle() / ROTATION_GEAR_RATIO

        color_dictionary[STRING_TO_COLOR_DICTIONARY[color]] = angle
    return color_dictionary
