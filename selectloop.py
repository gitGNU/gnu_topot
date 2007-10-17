from threading import Thread
import select
from time import time

def getFD(value):
  if hasattr(value, "fileno"):
    return value.fileno()
  else:
    return value

class SelectLoop (Thread):
  maxDelay = .2
  
  def __init__(self):
    Thread.__init__(self)
    self.setDaemon(True)
    self.in_fds = {}
    self.out_fds = {}
    self.timers = []

  def start(self):
    self.go = True
    Thread.start(self)

  def stop(self):
    self.go = False

  def register(self, gen):
    self.step(gen)

  def step(self, gen):
    try:
      command, value = gen.next()
      if command == "in":
        self.in_fds[getFD(value)] = gen
      elif command == "out":
        self.out_fds[getFD(value)] = gen
      elif command == "wait":
        self.addTimer(time() + value, gen)
      elif command == "time":
        self.addTimer(value, gen)
      else:
        raise Exception("Unknown SelectLoop command: " + command)
    except StopIteration:
      pass

  def addTimer(self, t, gen):
    pos = len(self.timers)
    for t_, gen_ in reversed(self.timers):
      if t_ >= t:
        break
      pos -= 1
    self.timers.insert(pos, (t, gen))

  def run(self):
    while self.go:
      delay = self.maxDelay
      if len(self.timers):
        delay = min(delay, self.timers[0][0])
        
      in_ready, out_ready, ex_ready = select.select(self.in_fds.keys(), self.out_fds.keys(),
                                                    [], delay)

      now = time()
      timers = []
      while len(self.timers) and self.timers[-1][0] <= now:
        timers.append(self.timers.pop())
      for t, gen in timers:
        self.step(gen)
        
      for in_fd in in_ready:
        gen = self.in_fds[in_fd]
        del self.in_fds[in_fd]
        self.step(gen)
        
      for out_fd in out_ready:
        gen = self.out_fds[out_fd]
        del self.in_fds[out_fd]
        self.step(gen)
