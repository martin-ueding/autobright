#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2017 Martin Ueding <dev@martin-ueding.de>

import argparse
import subprocess
import sys
import time

import numpy as np


def linear(x, a, b, c):
    #return a + b*x + c*x**2
    return a * np.exp(b * x) + c


def set_laptop_brightness(brightness):
    return
    command = ['xbacklight', '-set', str(max(10, brightness))]
    subprocess.call(command)


def set_brightness(brightness, device):
    if not 0 <= brightness <= 100:
        print('Brightness must be between 0 and 100.')
        sys.exit(1)

    command = ['ddccontrol',
               '-r', '0x10',
               '-w', str(brightness),
               'dev:/dev/i2c-' + device]

    status = subprocess.call(command)

    if status != 0:
        print('ddccontrol failed but it might still have worked')


def read_colorhug_als():
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


def auto_converter(reading):
    #popt = [0.00850944, -0.13749395]
    popt = [  8.73215023e+00,   5.69113822e-04,  -7]
    out = linear(reading, *popt)

    return max(min(out, 100), 0)


def main():
    options = _parse_args()

    weight = 0.4

    mean = None
    last_brightness = None

    steps = 0

    while True:
        reading = read_colorhug_als()

        if mean is None:
            mean = reading
        else:
            mean = weight * reading + (1 - weight) * mean

        print(reading, mean)

        steps += 1

        if steps == 5:
            target = auto_converter(mean)
            if target != last_brightness:
                print('Setting Brightness to', target)
                for device in options.device:
                    set_brightness(target, device)
                last_brightness = target
            steps = 0

        time.sleep(1)


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--device', default=['7'], nargs='+')
    options = parser.parse_args()

    return options


if __name__ == '__main__':
    main()
