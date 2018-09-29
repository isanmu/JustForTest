from myhdl import *

ACTIVE_LOW = bool(0)
FRAME_SIZE = 8
t_State = enum('SEARCH', 'CONFIRM', 'SYNC')  #  encoding='one_cold'


@block
def FramerCtrl(SOF, state, syncFlag, clk, reset_n, B, G, G2):

    """ Framing control FSM.

    SOF -- start-of-frame output bit
    state -- FramerState output
    syncFlag -- sync pattern found indication input
    clk -- clock input
    reset_n -- active low reset

    """

    index = Signal(intbv(0)[8:]) # position in frame

    @always(clk.posedge, reset_n.negedge)
    def FSM():
        if reset_n == ACTIVE_LOW:
            SOF.next = 0
            index.next = 0
            state.next = t_State.SEARCH
        else:
            index.next = (index + 1) % FRAME_SIZE
            SOF.next = 0
            if state == t_State.SEARCH:
                index.next = 1
                if syncFlag:
                    state.next = t_State.CONFIRM
            elif state == t_State.CONFIRM:
                if index == 0:
                    if syncFlag:
                        state.next = t_State.SYNC
                    else:
                        state.next = t_State.SEARCH
            elif state == t_State.SYNC:
                if index == 0:
                    if not syncFlag:
                        state.next = t_State.SEARCH
                SOF.next = (index == FRAME_SIZE-1)
            else:
                raise ValueError("Undefined state")

    @always_comb
    def logic():
        G.next = (B if B else B*2)
    @always_comb
    def logic2():
        G2.next = (B if B else B * 4)
    return FSM, logic, logic2


def convert(hdl):

    SOF = Signal(bool(0))
    syncFlag = Signal(bool(0))
    clk = Signal(bool(0))
    reset_n = Signal(bool(1))
    state = Signal(t_State.SEARCH)
    B = Signal(intbv(0)[4:].unsigned())
    G = Signal(intbv(0)[4:].unsigned())
    G2 = Signal(intbv(0)[4:].unsigned())

    inst = FramerCtrl(SOF, state, syncFlag, clk, reset_n, B, G, G2)
    inst.convert(hdl=hdl)
# toVerilog(FramerCtrl, SOF, state, syncFlag, clk, reset_n)
convert(hdl='Verilog')