#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>
# Licensed under The MIT License

import subprocess


def read():
    command = ['colorhug-cmd', 'set-multiplier', '20']
    subprocess.check_call(command)

    command = ['colorhug-cmd', 'set-color-select', 'white']
    subprocess.check_call(command)

    command = ['colorhug-cmd', 'take-reading-raw']
    output = subprocess.check_output(command).decode().strip()

    command = ['colorhug-cmd', 'set-multiplier', '0']
    subprocess.check_call(command)

    words = output.split()
    reading = int(words[1])
    return reading
