#!/usr/bin/env pybricks-micropython
from main import init, check_periodically_at


if __name__ == "__main__":
    init()
    check_periodically_at(1000, 0)
