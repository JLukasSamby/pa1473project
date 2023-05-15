#!/usr/bin/env pybricks-micropython
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.parameters import Color
from sorter_constants import MBOX_NAME, READY_MESSAGE, ERROR_MESSAGE
from init import init
from io import notify, configure_zones
from core import hold, item_in_place
from sort import sort
from constants import(CRANE_GEAR_RATIO,
                    ROTATION_GEAR_RATIO,
                    CRANE_RESTING_HIGH_ANGLE)
SERVER_NUM_ZONES = 3
from robot_setup import craneMotor, rotationMotor


def generate_server_color_dictionary(positions):
    return {
        Color.GREEN: positions[0],
        Color.YELLOW: positions[1],
        Color.RED: positions[2]
    }


if __name__ == "__main__":
    server = BluetoothMailboxServer()
    mbox = TextMailbox(MBOX_NAME, server)

    notify("Waiting for connection.")
    server.wait_for_connection()
    notify("Connected.")

    init()

    notify("Configure drop zones")
    positions = configure_zones(SERVER_NUM_ZONES, include_heights=True)
    color_dict = generate_server_color_dictionary(positions)
    notify("Drop zones configured")

    while True:
        while not item_in_place():
            notify("No item found.")
            notify("Waiting for item")
            hold()
        if not sort(color_dict, 0, include_heights=True):
            craneMotor.run_target(200,-CRANE_GEAR_RATIO*CRANE_RESTING_HIGH_ANGLE)
            rotationMotor.run_target(200, -90 * ROTATION_GEAR_RATIO)
            mbox.send(READY_MESSAGE)
            mbox.wait()
            message = mbox.read()
            if message == READY_MESSAGE:
                rotationMotor.run_target(200, 0)
            elif message == ERROR_MESSAGE:
                notify("Could not sort item")
                break
        notify("Waiting for next brick")
        hold()
