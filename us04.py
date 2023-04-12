#!/usr/bin/env pybricks-micropython
from main import init, pick_item, get_color, get_color_rgb, hold, drop_item


if __name__ == "__main__":
    init()
    pick_item()
    print("Color:", get_color())
    print("RGB:", get_color_rgb())
    drop_item()
    hold()
