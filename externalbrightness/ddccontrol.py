#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>
# Licensed under The MIT License

import subprocess


def set_brightness(brightness, device):
    if not 0 <= brightness <= 100:
        print('Brightness must be between 0 and 100.')
        sys.exit(1)

    command = ['ddccontrol',
               '-r', '0x10',
               '-w', str(brightness),
               'dev:/dev/i2c-{}'.format(device)]

    status = subprocess.call(command)

    if status != 0:
        print('ddccontrol failed but it might still have worked')
