#!/usr/bin/env pybricks-micropython
from main import clawMotor, LOW_SPEED, ev3
from pybricks.tools import wait
from pybricks.parameters import Button


if __name__ == "__main__":
    initial_angle = clawMotor.angle()
    while True:
        pressed = ev3.buttons.pressed()

        if Button.RIGHT in pressed:
            clawMotor.run(LOW_SPEED)
        elif Button.LEFT in pressed:
            clawMotor.run(-LOW_SPEED)
        else:
            clawMotor.hold()
        print(clawMotor.angle() - initial_angle)
        wait(100)