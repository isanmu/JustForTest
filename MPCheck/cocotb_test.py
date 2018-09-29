#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/29/2018 11:08
# @Author  : Winson
# @User    : winswang
# @Site    : 
# @File    : cocotb_test.py
# @Project : JustForTest
# @Software: PyCharm

import cocotb
from cocotb.triggers import Timer


@cocotb.test()
def my_first_test(dut):
    """
    Try accessing the design
    :param dut:
    """
    dut._log.info('Running test!')
    for cycle in range(10):
        dut.clk = 0
        yield Timer(1000)
        dut.clk = 1
        yield Timer(1000)
    dut._log.info('Running test!')
