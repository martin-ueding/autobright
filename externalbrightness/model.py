#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright © 2016 Martin Ueding <dev@martin-ueding.de>

import numpy as np


def linear(x, a, b, c):
    #return a + b*x + c*x**2
    return a * np.exp(b * x) + c


def auto_converter(reading):
    #popt = [0.00850944, -0.13749395]
    popt = [  8.73215023e+00,   5.69113822e-04,  -9]
    out = linear(reading, *popt)

    return max(min(out, 100), 0)
