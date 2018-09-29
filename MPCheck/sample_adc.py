#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 9/18/2018 16:08
# @Author  : Winson
# @User    : winswang
# @Site    : 
# @File    : sample_adc.py
# @Project : JustForTest
# @Software: PyCharm

from myhdl import block, always_comb, always_seq, Signal, intbv, \
                modbv, enum, ResetSignal, delay, StopSimulation, \
                always, instance, toVerilog

AD_State = enum(
    'AD_IDLE', 'AD_VIN', 'AD_VDIFF1', 'AD_VDIFF2', 'AD_IMON1', 'AD_IMON2',
    'AD_I1', 'AD_I2', 'AD_I3', 'AD_I4', 'AD_I5', 'AD_I6', 'AD_I7', 'AD_I8',
    'AD_I9', 'AD_I10', 'AD_I11', 'AD_I12', 'AD_I13', 'AD_I14', 'AD_I15',
    'AD_I16', 'AD_I17', 'AD_I18', 'AD_I19', 'AD_I20',
    'AD_VFB1', 'AD_VFB2', 'AD_TSNS1', 'AD_TSNS2', 'AD_ADDR', 'AD_VBE',
    'AD_VBOOT1', 'AD_VBOOT2', 'AD_VAUXSEN', encoding='one_hot'
)

CS_State = enum(
    'CS_I1', 'CS_I2', 'CS_I3', 'CS_I4', 'CS_I5', 'CS_I6', 'CS_I7', 'CS_I8',
    'CS_I9', 'CS_I10', 'CS_I11', 'CS_I12', 'CS_I13', 'CS_I14', 'CS_I15',
    'CS_I16', 'CS_I17', 'CS_I18', 'CS_I19', 'CS_I20',
    'CS_TSNS1', 'CS_TSNS2', 'CS_ADDR', 'CS_VBOOT1', 'CS_VBOOT2', 'CS_AUXSEN'
)

Channel_State = enum(
    'CHANL_VI33_BUF', 'CHANL_CS', 'CHANL_IMON1', 'CHANL_IMON2', 'CHANL_VIN',
    'CHANL_VDIFF1', 'CHANL_VFB1', 'CHANL_VDIFF2', 'CHANL_VFB2', 'CHANL_TEMP_VBE'
)

@block
def sample_adc(
        cal_active, adc_channel_mux, sample_busy, ad_trig, ad_channel,
        # cs_sel, vfb1_convert_done, vfb2_convert_done, vdiff1_convert_done,
        # vdiff2_convert_done, imon1_convert_done, imon2_convert_done,
        # vboot1_convert_done, vboot2_convert_done, addr_convert_done,
        ad_trig_self,
        # vin_sense,
        # vdiff1_sense,
        # vdiff2_sense,
        # imon1_sense,
        # imon2_sense,
        # vfb1_sense,
        # vfb2_sense,
        # i1_sense,
        # i2_sense,
        # i3_sense,
        # i4_sense,
        # i5_sense,
        # i6_sense,
        # i7_sense,
        # i8_sense,
        # i9_sense,
        # i10_sense,
        # i11_sense,
        # i12_sense,
        # i13_sense,
        # i14_sense,
        # i15_sense,
        # i16_sense,
        # i17_sense,
        # i18_sense,
        # i19_sense,
        # i20_sense,
        # vboot1_sense,
        # vboot2_sense,
        # vauxsen_sense,
        # addr_sense,
        # tsns1_sense,
        # tsns2_sense,
        # die_temp_sense,
        clk_20M,
        nRst,
        # pwm_risingedge,
        ad_convert_done,
        fault_busy,
        # ad_result,
        # addr_cfg_dn,
        MFR_ADC_HOLD_TIME,
        # DBG_VIN_INJECT,
        # IOUT_SNS_PH_OFS_R1,
        # IOUT_SNS_PH_OFS_R2,
        # MFR_TSENS2_AUX_SEL,
        # ph1_en,
        ph16_en
):
    # internal register
    current_state = Signal(AD_State.AD_IDLE)
    next_state = Signal(modbv(0, min=0, max=2**6))
    cnt_4us = Signal(intbv(0)[7:])
    busy1 = Signal(bool(0))
    busy2 = Signal(bool(0))
    # adc_channel_mux = Signal(bool(0))
    ad_channel_buf = Signal(modbv(0, min=0, max=2**5))
    # ad_trig_self = Signal(bool(0))
    ad_trig_pwm = Signal(bool(0))
    convert_done = Signal(bool(0))

    @always_seq(clk_20M.posedge, reset=nRst)
    def func_busy1():
        if ad_convert_done:
            busy1.next = 1
        elif cnt_4us == MFR_ADC_HOLD_TIME:
            busy1.next = 0

    @always_seq(clk_20M.posedge, reset=nRst)
    def func_busy2():
        if ad_trig:
            busy2.next = 1
        elif ad_convert_done:
            busy2.next = 0

    @always_comb
    def logic_sample_busy():
        sample_busy.next = busy2

    @always_seq(clk_20M.posedge, reset=nRst)
    def func_cnt_4us():
        if ad_convert_done:
            cnt_4us.next = 0
        else:
            cnt_4us.next = cnt_4us + 1

    @always_seq(clk_20M.posedge, reset=nRst)
    def func_ad_trig_self():
        if cnt_4us == intbv(80)[7:]:
            ad_trig_self.next = 1
        else:
            ad_trig_self.next = 0

    @always_comb
    def func_ad_trig():
        ad_trig.next = 0 if busy1 or busy2 or fault_busy else (ad_trig_pwm or ad_trig_self)
        pass

    @always_seq(clk_20M.posedge, reset=nRst)
    def func_state():
        current_state.next = next_state

    @always_comb
    def logic_convert_done():
        convert_done.next = ad_convert_done

    @always_comb
    def logic_state():
        if current_state == AD_State.AD_IDLE:
            if ad_trig:
                next_state = AD_State.AD_VIN
            else:
                next_state = AD_State.AD_IDLE
        elif current_state == AD_State.AD_VIN:
            if convert_done:
                next_state = AD_State.AD_VDIFF1
            else:
                next_state = AD_State.AD_VIN

    return func_busy1, func_busy2, func_ad_trig, func_ad_trig_self, func_cnt_4us, \
           logic_sample_busy, logic_convert_done, logic_state, func_state


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
MFR_ADC_HOLD_TIME = Signal(modbv(min=0, max=2**7))
ph16_en = Signal(bool(0))

sample_adc(
    cal_active, adc_channel_mux, sample_busy, ad_trig, ad_channel,
    # cs_sel, vfb1_convert_done, vfb2_convert_done, vdiff1_convert_done,
    # vdiff2_convert_done, imon1_convert_done, imon2_convert_done,
    # vboot1_convert_done, vboot2_convert_done, addr_convert_done,
    ad_trig_self,
    # vin_sense,
    # vdiff1_sense,
    # vdiff2_sense,
    # imon1_sense,
    # imon2_sense,
    # vfb1_sense,
    # vfb2_sense,
    # i1_sense,
    # i2_sense,
    # i3_sense,
    # i4_sense,
    # i5_sense,
    # i6_sense,
    # i7_sense,
    # i8_sense,
    # i9_sense,
    # i10_sense,
    # i11_sense,
    # i12_sense,
    # i13_sense,
    # i14_sense,
    # i15_sense,
    # i16_sense,
    # i17_sense,
    # i18_sense,
    # i19_sense,
    # i20_sense,
    # vboot1_sense,
    # vboot2_sense,
    # vauxsen_sense,
    # addr_sense,
    # tsns1_sense,
    # tsns2_sense,
    # die_temp_sense,
    clk_20M,
    nRst,
    # pwm_risingedge,
    ad_convert_done,
    fault_busy,
    # ad_result,
    # addr_cfg_dn,
    MFR_ADC_HOLD_TIME,
    # DBG_VIN_INJECT,
    # IOUT_SNS_PH_OFS_R1,
    # IOUT_SNS_PH_OFS_R2,
    # MFR_TSENS2_AUX_SEL,
    # ph1_en,
    ph16_en
).convert(hdl='Verilog')