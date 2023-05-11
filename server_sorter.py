#!/usr/bin/env pybricks-micropython
from main import (
    user_generate_color_dictionary,
    rotationMotor,
    ROTATION_GEAR_RATIO,
    sort,
    configure_zones,
    ev3
)
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.tools import wait
from pybricks.parameters import Color
from sorter import MBOX_NAME, READY_MESSAGE, ERROR_MESSAGE
from main import init

SERVER_NUM_ZONES = 3


def generate_server_color_dictionary(angles, heights=None):
    if heights is None:
        return {
            Color.GREEN: angles[0],
            Color.YELLOW: angles[1],
            Color.RED: angles[2]
        }
    else:
        return {
            Color.GREEN: (angles[0], heights[0]),
            Color.YELLOW: (angles[1], heights[1]),
            Color.RED: (angles[2], heights[2])
        }


if __name__ == "__main__":
    server = BluetoothMailboxServer()
    mbox = TextMailbox(MBOX_NAME, server)

    print("Waiting for connection...")
    ev3.screen.print("Waiting for connection...")
    server.wait_for_connection()
    print("Connected!")
    ev3.screen.print("Connected!")

    init()
    ev3.screen.print("init started")

    ev3.screen.print("Configure drop zones")
    (angles, heights) = configure_zones(SERVER_NUM_ZONES, include_heights=True)
    ev3.screen.print("Configured drop zones")
    color_dict = generate_server_color_dictionary(angles, heights)

    while True:
        is_sorted = sort(color_dict, 0, include_heights=True)
        if not is_sorted:
            rotationMotor.run_target(200, -90 * ROTATION_GEAR_RATIO)
            mbox.send(READY_MESSAGE)
            mbox.wait()
            message = mbox.read()
            if message == READY_MESSAGE:
                rotationMotor.run_target(200, 0)
            elif message == ERROR_MESSAGE:
                print("Could not sort item.")
                ev3.screen.print("Could not sort item")
                break
        print("Waiting for next brick...")
        ev3.screen.print("Waiting for next brick")
        wait(5000)
