#!/usr/bin/env pybricks-micropython
from main import init, pick_item, hold, drop_item_by_color, get_color, user_generate_color_dictionary


if __name__ == "__main__":
    color_dictionary = user_generate_color_dictionary()
    init()
    pick_item()
    color = get_color()
    print("Color:", color)
    drop_item_by_color(color, color_dictionary)
    hold()