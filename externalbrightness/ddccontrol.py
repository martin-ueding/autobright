#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2016 Martin Ueding <martin-ueding.de>
# Licensed under The MIT License

import subprocess


def set_brightness(brightness, device):
    assert 0 <= brightness <= 100, 'Brightness must be between 0 and 100.'

    command = ['ddccontrol',
               '-r', '0x10',
               '-w', str(brightness),
               'dev:/dev/i2c-{}'.format(device)]
    status = subprocess.call(command)

    if status != 0:
        print('ddccontrol failed but it might still have worked')


def set_maximum_color(red, green, blue, device):
    assert 0 <= red <= 100, 'Red must be between 0 and 100.'
    assert 0 <= green <= 100, 'Green must be between 0 and 100.'
    assert 0 <= blue <= 100, 'Blue must be between 0 and 100.'

    addresses = ['0x16', '0x18', '0x1a']

    for address, value in zip(addresses, [red, green, blue]):
        command = ['ddccontrol',
                   '-r', address,
                   '-w', str(value),
                   'dev:/dev/i2c-{}'.format(device)]
        status = subprocess.call(command)

        if status != 0:
            print('ddccontrol failed but it might still have worked')
