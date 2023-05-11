#!/usr/bin/env pybricks-micropython
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.parameters import Color
from sorter import MBOX_NAME, EXIT_MESSAGE, READY_MESSAGE, SERVER_NAME, ERROR_MESSAGE
from main import (
    init,
    rotationMotor,
    sort,
    configure_zones,
    notify,
    ev3
)


CLIENT_NUM_ZONES = 2


def generate_client_color_dictionary(positions):
    return {
        Color.BLACK: positions[0],
        Color.BLUE: positions[1],
    }


if __name__ == "__main__":
    ev3
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
            is_sorted = sort(color_dict, pick_up_zone, include_heights=True, sort_sign=-1)
            rotationMotor.run_target(-200, 0)
            if is_sorted:
                mbox.send(READY_MESSAGE)
            else:
                mbox.send(ERROR_MESSAGE)
