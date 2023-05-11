#!/usr/bin/env pybricks-micropython
from main import init, pick_item, hold, drop_item_by_color, get_color


if __name__ == "__main__":
    init()
    pick_item()
    color = get_color()
    print("Color:", color)
    drop_item_by_color(color)
    hold()
