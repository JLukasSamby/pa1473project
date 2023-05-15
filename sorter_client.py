#!/usr/bin/env pybricks-micropython
""" This module containts code for client(recvieng) robot"""
from pybricks.messaging import TextMailbox, BluetoothMailboxClient
from pybricks.parameters import Color
from sorter_constants import MBOX_NAME, READY_MESSAGE, ERROR_MESSAGE, SERVER_NAME, EXIT_MESSAGE
from init import init
from io import notify, configure_zones
from sort import sort
from robot_setup import rotationMotor


CLIENT_NUM_ZONES = 2


def generate_client_color_dictionary(positions):
    return {
        Color.BLACK: positions[0],
        Color.BLUE: positions[1],
    }


if __name__ == "__main__":
    client = BluetoothMailboxClient()
    mbox = TextMailbox(MBOX_NAME, client)

    notify("Establishing connection")
    client.connect(SERVER_NAME)
    notify("Connected")

    init()

    notify("Configure pick up")
    pick_up_zone = configure_zones(1)
    pick_up_zone = pick_up_zone[0]
    notify("Pick up configured")

    notify("Configure drop zones")
    positions = configure_zones(CLIENT_NUM_ZONES, include_heights=True)
    color_dict = generate_client_color_dictionary(positions)
    notify("Drop zones configured")

    while True:
        notify("Waiting for instruction")
        mbox.wait()
        message = mbox.read()
        if message == EXIT_MESSAGE:
            break
        if message == READY_MESSAGE:
            isSorted = sort(color_dict, pick_up_zone, include_heights=True, sort_sign=-1)
            rotationMotor.run_target(-200, 0)
            if isSorted:
                mbox.send(READY_MESSAGE)
            else:
                mbox.send(ERROR_MESSAGE)
