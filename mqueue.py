from Queue import Queue
from threading import Thread

class MQueue(Thread):
  queue = None
  clients = None
  go = False

  def __init__(self, start = False):
    Thread.__init__(self)
    self.setDaemon(True)
    self.queue = Queue(0)
    if start:
      self.start()

  def start(self):
    self.go = True
    Thread.start(self)

  def stop(self):
    self.go = False

  def run(self):
    while self.go:
      target, value = self.queue.get(True)
      target.signal(value)

  def send(self, target, value):
    self.queue.put((target, value))
