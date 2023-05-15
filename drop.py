#!/usr/bin/env pybricks-micropython
from pybricks.parameters import Stop
from constants import (
    HIGH_SPEED,
    CLAW_OPEN_ANGLE,
    MAX_DUTY,
    CRANE_GEAR_RATIO
)
from robot_setup import (
    clawMotor,
    craneMotor
)


def _drop() -> None:
    """
    Open claw to drop currently held item.
    """
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)

def drop_stalled() -> None:
    """
    Drop currently held item by running into the floor (stalling).
    """
    craneMotor.run_until_stalled(
        HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO
    )
    _drop()
    craneMotor.run_target(HIGH_SPEED, 0)


def drop_height(height: float) -> None:
    """
    Drop item using preconfigured height.
    
    Parameters:
        height (float): hegiht to drop at, given in angles of crane motor rotation.
    """
    craneMotor.run_target(HIGH_SPEED, height)
    _drop()
    craneMotor.run_target(HIGH_SPEED, 0)
