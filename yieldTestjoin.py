from myhdl import block, instance, intbv, delay, join, Signal, now, Simulation
@block
def test():
    # @instance
    def func1():
        for i in range(10):
            yield delay(10)
            print('func1 = %s' % i)

    # @instance
    def func2():
        for i in range(10):
            yield delay(5)
            print('func2 = %s' % i)

    @instance
    def func3():
        for i in range(5):
            print(i)
            yield join(func1(), func2())
    return func3#, func2, func1

# f = test()
# f.run_sim()


def trigger(event):
    event.next = not event


class Queue:
    def __init__(self):
        self.l = []
        self.sync = Signal(0)
        self.item = None

    def put(self, item):
        # non time-consuming method
        self.l.append(item)
        trigger(self.sync)

    def get(self):
        # time-consuming method
        if not self.l:
            print(self.sync)
            yield self.sync
        self.item = self.l.pop(0)


q = Queue()


def producer(q):
    yield delay(120)
    for i in range(15):
        print("%s: PUT item %s" % (now(), i))
        q.put(i)
        yield delay(max(5, 45 - 10 * i))


def consumer(q):
    yield delay(100)
    while 1:
        print("%s: TRY to get item" % now())
        yield q.get()
        print("%s: GOT item %s" % (now(), q.item))
        yield delay(30)


def main():
    p = producer(q)
    c = consumer(q)
    return p, c


sim = Simulation(main())
sim.run()
