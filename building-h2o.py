import threading
import random

class H2O(object):
    def __init__(self, lock):
        self.h = 0
        self.o = 0
        self.hc = threading.Condition(lock)
        self.oc = threading.Condition(lock)

    def H(self):
        self.hc.acquire()
        self.h += 1
        if self.h >= 2 and self.o >= 1:
            self.h -= 2
            self.o -= 1
            self.hc.notify()
            self.oc.notify()
            print "Generated H2O from H, %d H and %d O pending" % (self.h, self.o)
        else:
            self.hc.wait()
        self.hc.release()

    def O(self):
        self.oc.acquire()
        self.o += 1
        if self.h >= 2 and self.o >= 1:
            self.h -= 2
            self.o -= 1
            self.hc.notify()
            self.hc.notify()
            print "Generated H2O from O, %d H and %d O pending" % (self.h, self.o)
        else:
            self.oc.wait()
        self.oc.release()

h2o = H2O(threading.Lock())
items = range(30)
random.shuffle(items)
for i in items:
    # generate 20 Hs and 10 Os
    if i < 20:
        t = threading.Thread(target=h2o.H)
    else:
        t = threading.Thread(target=h2o.O)
    t.start()
