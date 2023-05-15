#!/usr/bin/env pybricks-micropython
""" This module containts sub-functions for pick activity """
from constants import (
    HIGH_SPEED,
    CLAW_OPEN_ANGLE,
    MAX_DUTY,
    CRANE_GEAR_RATIO
)
from robot_setup import clawMotor, craneMotor
from pybricks.parameters import Stop


def _open_claw() -> None:
    """Open claw."""
    clawMotor.run_target(HIGH_SPEED, CLAW_OPEN_ANGLE)

def _close_claw() -> None:
    """Close claw."""
    clawMotor.run_until_stalled(-HIGH_SPEED, then=Stop.HOLD, duty_limit=MAX_DUTY * 0.8)

def _pick_stalled() -> None:
    """Drop item using run_until_stalled."""
    _open_claw()
    craneMotor.run_until_stalled(
        HIGH_SPEED, then=Stop.COAST, duty_limit=MAX_DUTY / CRANE_GEAR_RATIO
    )
    _close_claw()
    craneMotor.run_target(HIGH_SPEED, 0)

def _pick_height(height: float) -> None:
    """Drop item using preconfigured height."""
    _open_claw()
    craneMotor.run_target(HIGH_SPEED, height)
    _close_claw()
    craneMotor.run_target(HIGH_SPEED, 0)
