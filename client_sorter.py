#!/usr/bin/env pybricks-micropython
from pybricks.messaging import BluetoothMailBoxClient, TextMailbox
from sorter import MBOX_NAME, EXIT_MESSAGE, READY_MESSAGE, SERVER_NAME, ERROR_MESSAGE
from main import (
    init,
    rotationMotor,
    user_generate_color_dictionary,
    sort,
    ROTATION_GEAR_RATIO,
)

if __name__ == "__main__":
    client = BluetoothMailBoxClient()
    mbox = TextMailbox(MBOX_NAME, client)

    print("Establishing connection...")
    client.connect(SERVER_NAME)
    print("Connected!")

    init()

    rotationMotor.stop()
    input("Press enter to select current position as pick-up zone.")
    pick_up_zone = -rotationMotor.angle() / ROTATION_GEAR_RATIO

    color_dict = user_generate_color_dictionary()

    while True:
        mbox.wait()
        message = mbox.read()
        if message == EXIT_MESSAGE:
            break
        if message == READY_MESSAGE:
            rotationMotor.run_target(200, pick_up_zone)
            is_sorted = sort(color_dict)
            rotationMotor.run_target(200, 0)
            if is_sorted:
                mbox.send(READY_MESSAGE)
            else:
                mbox.send(ERROR_MESSAGE)
