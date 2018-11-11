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

cmd = "iverilog -o bin2gray.o -Dwidth=%s " + \
      "bin2gray.v " + \
      "dut_bin2gray.v "
# cmd = "iverilog -s dut_bin2gray -o dut_bin2gray.out -Dwidth=%s -y " \
#       "C:/Users/sanmu/PycharmProjects/TestMyHDL dut_bin2gray.v "


def bin2gray(B, G):
    width = len(B)
    os.system(cmd % width)
    # return Cosimulation("C:/iverilog/bin/vvp.exe -M -m myhdl bin2gray.o", B=B, G=G)
    # print(os.path)
    # os.system("vvp -M ./ -m myhdl bin2gray") C:/Users/sanmu/PycharmProjects/TestMyHDL
    return Cosimulation("vvp -m .\myhdl64.vpi bin2gray.o", B=B, G=G)
