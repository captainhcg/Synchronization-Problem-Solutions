import threading
import random

class Bridge(object):
    def __init__(self, capacity):
        lock = threading.RLock()
        self.locks = [
            threading.Condition(lock),
            threading.Condition(lock)
        ]
        self.waiting = [0, 0]
        self.current_direction = None
        self.capacity = capacity
        self.cars = 0

    def arrive(self, direction):
        condition = self.locks[direction]
        condition.acquire()
        while self.cars >= self.capacity or (self.cars != 0 and self.current_direction != direction):
            print "car with direction %d is waiting, current direction %s, cars %d, waiting list %s" % (direction, self.current_direction, self.cars, self.waiting)
            self.waiting[direction] += 1
            condition.wait()
            self.waiting[direction] -= 1
        self.cars += 1
        self.current_direction = direction
        print "car with direction %d is on the bridge, current direction %s, cars %d, waiting list %s" % (direction, self.current_direction, self.cars, self.waiting)
        condition.release()
        self.exit(direction)

    def exit(self, direction):
        condition = self.locks[direction]
        condition.acquire()
        self.cars -= 1
        print "car with direction %d is off the bridge, current direction %s, cars %d, waiting list %s" % (direction, self.current_direction, self.cars, self.waiting)
        if self.waiting[direction]:
            condition.notify()
        else:
            self.locks[1 - direction].notifyAll()
        condition.release()

bridge = Bridge(3)  # default set to 3
cars = range(30)
random.shuffle(cars)
for idx, car in enumerate(cars):
    # generate 15 P and 15 V
    print "%d car arrived, direction %s" % (idx, car % 2)
    t = threading.Thread(target=bridge.arrive, args=(car % 2,))
    t.start()
