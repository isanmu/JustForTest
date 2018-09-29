#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/28/2018 15:01
# @Author  : Winson
# @User    : winswang
# @Site    : 
# @File    : cosim_bin2gray.py
# @Project : JustForTest
# @Software: PyCharm

import os

from myhdl import Cosimulation

cmd = r"C:\iverilog\bin\iverilog.exe -o bin2gray.o -Dwidth=%s " + \
      "./MPCheck/bin2gray.v " + \
      "./MPCheck/dut_bin2gray.v "


def bin2gray(B, G):
    width = len(B)
    os.system(cmd % width)
    return Cosimulation(r"C:\iverilog\bin\vvp.exe -m C:\Users\winswang\PycharmProjects\JustForTest\MPCheck\myhdl bin2gray.o", B=B, G=G)