# Central event management module. An instance of the Topot class is
# created by applications and used as a central place for creating
# signals. The responsibilities of the object are:
#
# * Running the main loop thread -- handled by SelectLoop
# * Managing the naming of signals.
# * Handling modifiers.
#
# After a Topot has been created, in- and output modules can be added
# to it with the add method. Such a module should have a start method,
# which takes the topot object as its argument, and registers its
# signal types under the appropriate names using the registerInput and
# registerOutput methods, which take a string (naming the signal) and
# a function (used to create signal objects of that type) as
# arguments. Add can be given a second argument, a string to be
# prefixed to all signal types registered by this module.
#
# When modules have been registered, signals can be connected with the
# Topot object's connect method. The first argument to this method is
# a string naming the output signal, followed by zero or more
# arguments that should be passed to function that creates this
# signal, and finally the input signal that it should be connected to.
# This input signal will usually be created using the get method,
# whose first argument is the name of the signal, again followed by
# extra parameters that should be passed to the signal-creator. For
# example:
#
# t = Topot()
# t.add(xkey.Keys())
# t.add(xrobot.XRobot(20))
# t.connect("key", 38, t.get("key", 66))
#
# ... will connect key 66 (caps lock) to key 38 (a).
#
# The topot object is started using its start method, and stopped
# again with the stop method.
#
# Modifiers are signals that block or allow other signals. When the
# withModifiers method of a Topot object is called, all signals
# connected until the clearModifiers method is called will be effected
# by the given modifiers. withModifiers takes two keyword arguments,
# 'on' and 'off', each of which should be an array of modifier names
# that should be active or inactive for the subsequently defined
# connections to work. Signals connected to the (always available)
# "mod" type of output signals determine which modifiers are active.
# The name of the modifier is given as an argument, for example, this
# will bind the control key to modifier "ctrl":
#
# t.connect("mod", "ctrl", t.get("key", 37))

from selectloop import SelectLoop
from signals import *

def nameSignal(signal, id, args):
  signal.name = id + " " + " ".join([repr(x) for x in args])
  return signal


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
    return nameSignal(result, outputid, specs)

  def get(self, id, *specs):
    input = self.inputSignals[id](*specs)
    result = None
    if (self.selectedModifiers):
      checker = self.selectedModifiers
      def checkModifier(prevValue):
        if checker(self.modifier.value):
          return input.value
        else:
          return prevValue
      result = Signal(checkModifier, input, self.modifier, init=input.value)
    else:
      result = input
    return nameSignal(result, id, specs)
