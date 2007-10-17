from selectloop import SelectLoop
from signals import *

class Topot (SelectLoop):
  selectedModifiers = None

  def __init__(self):
    SelectLoop.__init__(self)
    self.inputSignals = {}
    self.outputSignals = {"mod": self.activateModifier}
    self.connected = []
    self.components = []
    self.modifier = InputSignal(set([None]))
    
  def add(self, component, prefix = ""):
    self.prefix = prefix
    self.components.append(component)
    gen = component.start(self)
    if gen: self.register(gen)
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
    return OutputSignal(setModifier, input)

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
      def checkModifier(prevValue, initialized):
        if (not initialized) or checker(self.modifier.value):
          return input.value
        else:
          return prevValue
      return Signal(checkModifier, input, self.modifier)
    else:
      return input
