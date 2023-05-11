#!/usr/bin/env pybricks-micropython
from main import init, configure_height_and_angle_positions, pick_item_at_height, drop_item_at_height


if __name__ == "__main__":
    init()
    rotation_angle, crane_angle = configure_height_and_angle_positions()
    drop_off_zones = []
    for _ in range(2):
        drop_off_zones.append(tuple(configure_height_and_angle_positions()))

    for drop_off_zone in drop_off_zones:
        pick_item_at_height(rotation_angle, crane_angle)
        drop_item_at_height(*drop_off_zone)
