#!/usr/bin/env pybricks-micropython
from core import item_in_place, pick, drop, get_color,hold
from constants import COLOR_DICTIONARY
from io import notify



def check_periodically_at(period, angle):
    """Check if item at designated angle at every period (ms)."""
    while True:
        if item_in_place(angle):
            notify("Item found.")
        else:
            notify("No item found.")
        hold(period)


def sort_periodically_at(period, angle, color_dictionary=COLOR_DICTIONARY):
    """Check if item at designated angle at every period (ms)."""
    while True:
        sort(color_dictionary, angle)
        hold(period)


def sort(color_dictionary, angle=0, include_heights=False, sort_sign=1):
    pick(angle=angle)
    color = get_color()
    if color not in color_dictionary:
        drop(angle=angle)
        return False
    if include_heights:
        drop(angle=sort_sign * color_dictionary[color][0], height=color_dictionary[color][1])
    else:
        drop(angle=sort_sign*color_dictionary[color])
    return True
