from swig import grabkey
from threading import Thread
from cell import *

Shift = grabkey.ShiftMask
Control = grabkey.ControlMask
Alt = grabkey.Mod1Mask
Any = grabkey.AnyModifier

class KeyCell(InputCell):
  def __init__(self, reset):
    InputCell.__init__(self, 0)
    self.reset = reset

  def __del__(self):
    self.reset()

class Keys(Thread):
  handlers = None

  def __init__(self):
    Thread.__init__(self)
    self.setDaemon(True)
    self.handlers = {}

  def __del__(self):
    self.reset()

  def start(self, topot):
    self.topot = topot
    topot.registerInput("key", self.cell)
    Thread.start(self)
    
  def run(self):
    while True:
      self.topot.enqueue(self.signal, grabkey.getEvent())

  def signal(self, event):
    type, keycode, modifiers, value = event
    if self.handlers.has_key((keycode, modifiers)):
      self.handlers[(keycode, modifiers)].value = value
    if self.handlers.has_key((keycode, Any)):
      self.handlers[(keycode, Any)].value = value

  def cell(self, keycode, modifiers = Any):
    name = (keycode, modifiers)
      
    if self.handlers.has_key(name):
      return self.handlers[name]
    else:
      handler = KeyCell(lambda: self.reset(keycode, modifiers))
      self.handlers[name] = handler
      grabkey.grabKey(keycode, modifiers, False)
      return handler

  def reset(self, keycode = None, modifiers = Any):
    if keycode is None:
      while len(self.handlers):
        key, handler = self.handlers.popitem()
        handler.reset()
        handler.reset = lambda: None
    else:
      grabkey.ungrabKey(keycode, modifiers)
      if self.handlers.has_key((keycode, modifiers)):
        del self.handlers[(keycode, modifiers)]
