#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/19/2018 14:55
# @Author  : Winson
# @User    : winswang
# @Site    : 
# @File    : test_casez.py
# @Project : JustForTest
# @Software: PyCharm

from myhdl import block, always_comb, always_seq, Signal, intbv, \
                modbv, enum, ResetSignal, delay, StopSimulation, \
                always, instance, toVerilog

AD_State = enum(
    'AD_IDLE', 'AD_VIN', 'AD_VDIFF1', 'AD_VDIFF2', encoding='one_hot'
)  # , encoding='one_hot'

@block
def sample_adc(
        ad_trig,
        clk_20M,
        nRst,
        ad_convert_done,
        outstate
):
    # internal register
    current_state = Signal(AD_State.AD_IDLE)
    next_state = Signal(AD_State.AD_IDLE)
    convert_done = Signal(bool(0))

    @always_seq(clk_20M.posedge, reset=nRst)
    def func_state():
        current_state.next = next_state

    @always_comb
    def logic_convert_done():
        convert_done.next = ad_convert_done

    @always_comb
    def logic_outstate():
        outstate.next = next_state

    @always_comb
    def logic_state():
        if current_state == AD_State.AD_IDLE:
            if ad_trig:
                next_state.next = AD_State.AD_VIN
            else:
                next_state.next = AD_State.AD_IDLE
        elif current_state == AD_State.AD_VIN:
            if convert_done:
                next_state.next = AD_State.AD_VDIFF1
            else:
                next_state.next = AD_State.AD_VIN
        elif current_state == AD_State.AD_VDIFF1:
            if convert_done:
                next_state.next = AD_State.AD_VDIFF2
            else:
                next_state.next = AD_State.AD_VDIFF1
        elif current_state == AD_State.AD_VDIFF2:
            if convert_done:
                next_state.next = AD_State.AD_VIN
            else:
                next_state.next = AD_State.AD_VDIFF2

    return logic_convert_done, logic_state, func_state, logic_outstate


cal_active = Signal(modbv(min=0, max=2**6))
adc_channel_mux = Signal(bool(0))
sample_busy = Signal(bool(0))
ad_trig = Signal(bool(0))
ad_channel = Signal(modbv(min=0, max=2**5))
ad_trig_self = Signal(bool(0))
clk_20M = Signal(bool(0))
nRst = ResetSignal(0, active=0, async=True)
ad_convert_done = Signal(bool(0))
fault_busy = Signal(bool(0))
outstate = Signal(AD_State.AD_IDLE)

sample_adc(
    ad_trig,
    clk_20M,
    nRst,
    ad_convert_done,
    outstate
).convert(hdl='Verilog')
