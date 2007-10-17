from threading import Thread
import select

def getFD(value):
  if hasattr(value, "fileno"):
    return value.fileno()
  else:
    return value
  

class SelectLoop (Thread):
  def __init__(self):
    Thread.__init__(self)
    self.setDaemon(True)
    self.in_fds = {}
    self.out_fds = {}

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
    except StopIteration:
      pass

  def run(self):
    while self.go:
      in_ready, out_ready, ex_ready = select.select(self.in_fds.keys(), self.out_fds.keys(), [])
      for in_fd in in_ready:
        gen = self.in_fds[in_fd]
        del self.in_fds[in_fd]
        self.step(gen)
      for out_fd in out_ready:
        gen = self.out_fds[out_fd]
        del self.in_fds[out_fd]
        self.step(gen)
