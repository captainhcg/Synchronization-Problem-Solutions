import threading
import random

class Semaphore(object):
    def __init__(self, counter):
        self.condition = threading.Condition()
        self.waiters = 0
        self.counter = counter

    def P(self):
        self.condition.acquire()
        if self.counter > 0:
            self.counter -= 1
            print "P consumes counter, counter %d, waiters %d" % (self.counter, self.waiters)
        else:
            self.waiters += 1
            print "P is waiting, counter %d, waiters %d" % (self.counter, self.waiters)
            self.condition.wait()
            print "P resumed, counter %d, waiters %d" % (self.counter, self.waiters)

        self.condition.release()

    def V(self):
        self.condition.acquire()
        if self.waiters > 0:
            self.waiters -= 1
            print "V notifies P, counter %d, waiters %d" % (self.counter, self.waiters)
            self.condition.notify()
            print "V was consumed, counter %d, waiters %d" % (self.counter, self.waiters)
        else:
            self.counter += 1
            print "V increments counter, counter %d, waiters %d" % (self.counter, self.waiters)
        self.condition.release()

semaphore = Semaphore(3)  # default set to 3
items = range(30)
random.shuffle(items)
for i in items:
    # generate 15 P and 15 V
    if i < 15:
        t = threading.Thread(target=semaphore.P)
    else:
        t = threading.Thread(target=semaphore.V)
    t.start()
