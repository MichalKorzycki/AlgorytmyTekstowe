import select
import sys
import time


def print_time(scheduler):
    print(time.ctime())
    scheduler.run_after(print_time, 5)


def echo_input(scheduler):
    message, _, _ = select.select([sys.stdin], [], [], 0)
    if message:
        message = input()
        print(message.upper())
    scheduler.run_soon(echo_input)


class Scheduler:
    def __init__(self):
        self.ready = []
        self.waiting = []

    def run_soon(self, task):
        self.waiting.append((task, 0))

    def run_after(self, task, delay):
        self.waiting.append((task, time.time() + delay))

    def run_until_complete(self):
        while self.ready or self.waiting:
            while self.ready:
                self.ready.pop()(self)
            for i in range(len(self.waiting) - 1, -1, -1):
                task, start_after = self.waiting[i]
                if start_after < time.time():
                    self.ready.append(task)
                    del self.waiting[i]


s = Scheduler()
s.run_soon(print_time)
s.run_soon(echo_input)
s.run_until_complete()
