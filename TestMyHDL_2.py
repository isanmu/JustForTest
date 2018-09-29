from myhdl import block, always_seq, Signal, intbv, modbv, enum, \
    ResetSignal, delay, StopSimulation, always, instance, toVerilog

ACTIVE_LOW = 0
FRAME_SIZE = 8
t_state = enum('SEARCH', 'CONFIRM', 'SYNC')


@block
def framer_ctrl(sof, state, sync_flag, clk, reset_n):
    """ Framing control FSM.

    sof -- start-of-frame output bit
    state -- FramerState output
    sync_flag -- sync pattern found indication input
    clk -- clock input
    reset_n -- active low reset

    """
    index = Signal(modbv(0, min=0, max=FRAME_SIZE))

    @always_seq(clk.posedge, reset=reset_n)
    def FSM():
        if reset_n == ACTIVE_LOW:
            sof.next = 0
            index.next = 0
            state.next = t_state.SEARCH
        else:
            index.next = (index + 1) % FRAME_SIZE
            sof.next = 0

            if state == t_state.SEARCH:
                index.next = 1
                if sync_flag:
                    state.next = t_state.CONFIRM

            elif state == t_state.CONFIRM:
                if index == 0:
                    if sync_flag:
                        state.next = t_state.SYNC
                    else:
                        state.next = t_state.SEARCH
            elif state == t_state.SYNC:
                if index == 0:
                    if not sync_flag:
                        state.next = t_state.SEARCH
                sof.next = (index == FRAME_SIZE-1)
                # if index == FRAME_SIZE-1:
                #     sof.next = 1
                # else:
                #     sof.next = 0

            else:
                raise ValueError('Undefined state')
    return FSM

@block
def testbench():

    sof = Signal(bool(0))
    sync_flag = Signal(bool(0))
    clk = Signal(bool(0))
    reset_n = ResetSignal(1, active=ACTIVE_LOW, async=True)
    state = Signal(t_state.SEARCH)

    framer_ctrl_0 = framer_ctrl(sof, state, sync_flag, clk, reset_n)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        for i in range(3):
            yield clk.negedge
        for n in (12, 8, 8, 4):
            sync_flag.next = 1
            yield clk.negedge
            sync_flag._next = 0
            for i in range(n-1):
                yield clk.negedge
        raise StopSimulation

    return framer_ctrl_0, clkgen, stimulus


tb = testbench()
tb.config_sim(trace=True)
tb.run_sim()
sof = Signal(bool(0))
sync_flag = Signal(bool(0))
clk = Signal(bool(0))
state = Signal(t_state.SEARCH)
reset_n = ResetSignal(1, active=ACTIVE_LOW, async=True)
framer_ctrl(sof, state, sync_flag, clk, reset_n).convert(hdl='Verilog')


class MyObj(object):
   def __init__(self):
      self.x = Signal(intbv(0)[8:])
      self.y = Signal(intbv(0)[4:])
      self.z = Signal(intbv(0)[9:])

clk = Signal(False)
xyz = MyObj()

@block
def m_ex1(clk, xyz):

   @always(clk.posedge)
   def hdl():
      xyz.z.next = xyz.x + xyz.y

   return hdl


m_ex1(clk, xyz).convert(hdl='Verilog')

