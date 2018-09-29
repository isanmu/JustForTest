from myhdl import block, instance, delay, always, now, Signal, instances
from myhdl import intbv, bin, modbv, StopSimulation

@block
def ClkDriver(clk, period=20):
    lowTime = int(period/2)
    hightime = period - lowTime

    @instance
    def drive_clk():
        while True:
            yield delay(lowTime)
            clk.next = 1
            yield delay(hightime)
            clk.next = 0
    return drive_clk

@block
def helloworld(clk, to='World'):
    # clk = Signal(0)
    # a = Signal(modbv(0, -1, 2**1))
    # b = Signal(0)
    count = Signal(intbv(0)[4:])

    # @always(delay(10))
    # def drive_clk():
    #     a.next = a+1              # sequence
    #     b.next = a+1            # sequence
    #     # a.next = b           # concurrency
    #     # b.next = a           # concurrency
    #     print(bin(a, width=3), a.max, bin(b))        # sequence
    #     clk.next = not clk   # concurrency

    @always(clk.posedge)
    def say_hello():
        # count.next = count + 1
        print('Hello count= %s' % count)
        # print("%s Hello %s!" % (now(), to))

    @instance
    def test():
        count.next = count + 1
        # print('now= %s, Test Count1 = %s' % (now(), count))
        # print(type(clk.posedge))
        yield clk.posedge
        yield delay(1)
        # raise ValueError('Undefined state')
        print('now= %s, Test Count = %s' % (now(), count))

    return say_hello, test  # drive_clk

@block
def Greetings():
    clk1 = Signal(bool(0))
    clk2 = Signal(bool(0))

    clkdriver_1 = ClkDriver(clk1)
    clkdriver_2 = ClkDriver(clk=clk2, period=19)
    hello_1 = helloworld(clk=clk1)
    hello_2 = helloworld(to="MyHDL", clk=clk2)

    return clkdriver_1, clkdriver_2, hello_1, hello_2
    # return instances()

# clk = Signal(0)
# inst = helloworld()
inst = Greetings()
# inst.run_sim(50)
inst.convert(hdl='Verilog')
inst.verify_convert()


# a = intbv(24)
# print(bin(12))
