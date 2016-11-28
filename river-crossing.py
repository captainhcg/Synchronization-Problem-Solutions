import threading
import random

class Boat(object):
    def __init__(self):
        self.assignedH = 0
        self.assignedE = 0
        self.waitingH = 0
        self.waitingE = 0
        lock = threading.Lock()
        self.Hc = threading.Condition(lock)
        self.Ec = threading.Condition(lock)

    def arriveH(self):
        self.Hc.acquire()
        self.waitingH += 1
        if self.waitingH >= 2:
            self.waitingH -= 2
            self.assignedH += 2
            if self.assignedH + self.assignedE >= 4:
                self.row("H")
            self.Hc.notify()
        else:
            self.Hc.wait()
        self.Hc.release()

    def arriveE(self):
        self.Ec.acquire()
        self.waitingE += 1
        if self.waitingE >= 2:
            self.waitingE -= 2
            self.assignedE += 2
            if self.assignedH + self.assignedE >= 4:
                self.row("E")
            self.Ec.notify()
        else:
            self.Ec.wait()
        self.Ec.release()

    def row(self, person):
        print "Last person %s, %s hackers and %s employees row. %s hackers and %s employees waiting." % (person, self.assignedH, self.assignedE, self.waitingH, self.waitingE)
        self.assignedE = self.assignedH = 0

boat = Boat()
people = range(32)
random.shuffle(people)
for p in people:
    # 12 hackers and 20 employees
    if p < 12:
        t = threading.Thread(target=boat.arriveH)
    else:
        t = threading.Thread(target=boat.arriveE)
    t.start()
