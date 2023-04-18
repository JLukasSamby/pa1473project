#!/usr/bin/env pybricks-micropython
from main import *
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from sorter import MAILBOX_NAME
from main import init


if __name__ == "__main__":
    server = BluetoothMailboxClient()
    mbox = TextMailbox(MAILBOX_NAME, server)

    print('Waiting for connection...')
    server.wait_for_connection()
    print('Connected!')

    init()

    color_dict = user_generate_color_dictionary()

    while True:
        is_sorted = sort()
        if not is_sorted:
            rotationMotor.run_target(200, -90 * ROTATION_GEAR_RATIO)
            mbox.send(READY_MESSAGE)
            message = mbox.read()
            if message == READY_MESSAGE:
                rotationMotor.run_target(200, 0)
            elif message == ERROR_MESSAGE:
                print("Could not sort item.")
                break
        wait(5000)

