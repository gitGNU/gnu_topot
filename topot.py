from threading import Thread
from Queue import Queue

class Topot:
  thread = None
  go = True

  def __init__(self, useThread = True):
    self.queue = Queue(0)
    self.inputSignals = {}
    self.outputSignals = {}
    self.connected = []
    self.components = []
    
    if useThread:
      self.thread = Thread()
      self.thread.setDaemon(True)
      self.thread.run = self.run

  def start(self):
    self.go = True
    if self.thread:
      self.thread.start()
    else:
      self.run()

  def stop(self):
    self.go = False

  def run(self):
    while self.go:
      self.queue.get(True)()

  def enqueue(self, thunk, *args):
    def delayed():
      return thunk(*args)
    if len(args) > 0:
      self.queue.put(delayed)
    else:
      self.queue.put(thunk)

  def add(self, component, prefix = ""):
    self.prefix = prefix
    self.components.append(component)
    component.start(self)
    self.prefix = ""

  def registerInput(self, id, callback):
    self.inputSignals[self.prefix + id] = callback
  def registerOutput(self, id, callback):
    self.outputSignals[self.prefix + id] = callback

  def connect(self, outputid, *args):
    specs = args[:-1]
    input = args[-1]
    return self.outputSignals[outputid](input, *specs)

  def get(self, id, *specs):
    connection = self.inputSignals[id](*specs)
    self.connected.append(connection)
    return connection
