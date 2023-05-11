#!/usr/bin/env pybricks-micropython
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.parameters import Color
from sorter import MBOX_NAME, EXIT_MESSAGE, READY_MESSAGE, SERVER_NAME, ERROR_MESSAGE
from main import (
    init,
    rotationMotor,
    user_generate_color_dictionary,
    sort,
    ROTATION_GEAR_RATIO,
    configure_zones,
    ev3,
    reset_position
)


CLIENT_NUM_ZONES = 2


def generate_client_color_dictionary(positions):
    return {
        Color.BLACK: positions[0],
        Color.BLUE: positions[1],
    }


if __name__ == "__main__":
    client = BluetoothMailboxClient()
    mbox = TextMailbox(MBOX_NAME, client)

    print("Establishing connection...")
    ev3.screen.print("Establishing connection...")
    ev3.speaker.say("Establishing connection...")
    client.connect(SERVER_NAME)
    print("Connected!")
    ev3.screen.print("Connected")
    ev3.speaker.say("Connected")

    init()

    ev3.screen.print("Configure pick up")
    ev3.speaker.say("Configure pick up")
    pick_up_zone = configure_zones(1)
    pick_up_zone = pick_up_zone[0]
    ev3.screen.print("Configured pick up")
    ev3.speaker.say("Configured pick up")

    ev3.screen.print("Configure drop zones")
    positions = configure_zones(CLIENT_NUM_ZONES, include_heights=True)
    ev3.screen.print("Configured drop zones")
    color_dict = generate_client_color_dictionary(positions)

    while True:
        ev3.screen.print("Waiting for instruction")
        mbox.wait()
        message = mbox.read()
        if message == EXIT_MESSAGE:
            break
        if message == READY_MESSAGE:
            # rotationMotor.run_target(200, -pick_up_zone * ROTATION_GEAR_RATIO)
            is_sorted = sort(color_dict, pick_up_zone, include_heights=True)
            reset_position()
            if is_sorted:
                mbox.send(READY_MESSAGE)
            else:
                mbox.send(ERROR_MESSAGE)
