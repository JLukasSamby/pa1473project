#!/usr/bin/env pybricks-micropython
from main import init, pick_item_at, get_color, get_color_rgb, hold, drop_item_at, configure_height_and_angle_positions

if __name__ == "__main__":
    init()
    angle_rotation, angle_crane = configure_height_and_angle_positions()
    pick_item_at(angle_rotation)
    print("Color:", get_color())
    print("RGB:", get_color_rgb())
    drop_item_at(angle_rotation)
    hold()
