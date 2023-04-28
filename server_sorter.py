#!/usr/bin/env pybricks-micropython
from main import (
    user_generate_color_dictionary,
    rotationMotor,
    ROTATION_GEAR_RATIO,
    sort,
    configure_zones
)
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.tools import wait
from pybricks.parameters import Color
from sorter import MBOX_NAME, READY_MESSAGE, ERROR_MESSAGE
from main import init

SERVER_NUM_ZONES = 3


def generate_server_color_dictionary(positions):
    return {
        Color.GREEN: positions[0],
        Color.YELLOW: positions[1],
        Color.RED: positions[2]
    }


if __name__ == "__main__":
    server = BluetoothMailboxServer()
    mbox = TextMailbox(MBOX_NAME, server)

    print("Waiting for connection...")
    server.wait_for_connection()
    print("Connected!")

    init()

    positions = configure_zones(SERVER_NUM_ZONES)
    color_dict = generate_server_color_dictionary(positions)

    while True:
        is_sorted = sort(color_dict)
        if not is_sorted:
            rotationMotor.run_target(200, -90 * ROTATION_GEAR_RATIO)
            mbox.send(READY_MESSAGE)
            message = mbox.read()
            if message == READY_MESSAGE:
                rotationMotor.run_target(200, 0)
            elif message == ERROR_MESSAGE:
                print("Could not sort item.")
                break
        print("Waiting for next brick...")
        wait(5000)
