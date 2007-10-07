from threading import Thread
from Queue import Queue
from cell import *

class Topot:
  thread = None
  go = True
  selectedModifiers = None

  def __init__(self, useThread = True):
    self.queue = Queue(0)
    self.inputSignals = {}
    self.outputSignals = {"mod": self.activateModifier}
    self.connected = []
    self.components = []
    self.modifier = InputCell(set([None]))
    
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

  # Used by signal-connecting code
  def withModifiers(self, on=[], off=[]):
    _on = set(on)
    _off = set(off)
    def check(current):
      return _on.issubset(current) and len(current & _off) == 0
    self.selectedModifiers = check
  def clearModifiers(self):
    self.selectedModifiers = None

  def registerInput(self, id, callback):
    self.inputSignals[self.prefix + id] = callback
  def registerOutput(self, id, callback):
    self.outputSignals[self.prefix + id] = callback

  # Used by signals themselves
  def activateModifier(self, input, modifier):
    modifier = set([modifier])
    def setModifier():
      if input.value:
        self.modifier.value = self.modifier.value | modifier
      else:
        self.modifier.value = self.modifier.value - modifier
    return OutputCell(setModifier, input)

  def connect(self, outputid, *args):
    specs = args[:-1]
    input = args[-1]
    result = self.outputSignals[outputid](input, *specs)
    self.connected.append(result)
    return result

  def get(self, id, *specs):
    input = self.inputSignals[id](*specs)
    if (self.selectedModifiers):
      checker = self.selectedModifiers
      def checkModifier():
        if (not checkModifier.cell.initialized) or checker(self.modifier.value):
          return input.value
        else:
          return checkModifier.cell.value
      return Cell(checkModifier, input, self.modifier)
    else:
      return input
