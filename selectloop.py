# Object to make single-threaded event-dispatching easier. Like the
# Twisted framework, this allows a bunch of different processes that
# all need to wait for file descriptors (sockets, pipes) to coexist in
# one thread. It uses generators to make it easy to write these
# processes. A generator is added to the loop with the register
# method, which calls its next method. When the generator yields an
# (command, value) pair, it is suspended until the event denoted by
# that pair happens. The following commands are supported:
#
# ("in", filedesc) : Suspend until input is available in the given file.
# ("out", filedesc): Suspend until the given file is available for output.
#                    given file.
# ("wait", seconds): Suspend for the given amount of seconds.
# ("time", seconds): Suspend until time.time() returns a certain
#                    amount of seconds.

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
        delay = min(delay, max(.001, self.timers[0][0] - time()))
        
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
