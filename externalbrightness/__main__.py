#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

import argparse

from . import model
from . import colorhugals
from . import ddccontrol


def main_set(options):
    print(options)

    if options.green is not None:
        for device in options.device:
            ddccontrol.set_maximum_color(options.red, options.green, options.blue, device)

    if options.brightness is None:
        reading = colorhugals.read()
        set_to = model.auto_converter(reading)
        print('I read {} and I will set to {}.'.format(reading, set_to))
    else:
        set_to = options.brightness

    for device in options.device:
        ddccontrol.set_brightness(set_to, device)


def main(options):
    print(options)


def _parse_args():
    '''
    Parses the command line arguments.

    :return: Namespace with arguments.
    :rtype: Namespace
    '''
    parser = argparse.ArgumentParser(description='')
    parser.set_defaults(func=main)
    subparsers = parser.add_subparsers(title='Commands', help='Sub-command help')

    parser_set = subparsers.add_parser('set', help='Manual brightness setting')
    parser_set.add_argument('--device', type=int, nargs='+', help='Device numbers for /dev/i2c-X')
    parser_set.add_argument('--brightness', type=int, help='Do not query ColorHugALS and use given brightness value')
    parser_set.add_argument('--red', type=int)
    parser_set.add_argument('--green', type=int)
    parser_set.add_argument('--blue', type=int)
    parser_set.set_defaults(func=main_set)

    options = parser.parse_args()
    options.func(options)


if __name__ == '__main__':
    _parse_args()
