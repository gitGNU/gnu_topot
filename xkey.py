from swig import grabkey
from swig import robot # for X display handling
from signals import *
from weakref import ref

Shift = grabkey.ShiftMask
Control = grabkey.ControlMask
Alt = grabkey.Mod1Mask
Any = grabkey.AnyModifier

class Keys:
  handlers = None

  def __init__(self):
    self.handlers = {}
    self.display = robot.openDisplay()

  def __del__(self):
    robot.closeDisplay(self.display)
    self.reset()

  def start(self, topot):
    topot.registerInput("key", self.key)
    return self.run()
    
  def run(self):
    while True:
      yield ("in", robot.displayFD(self.display))
      while True:
        event = grabkey.checkEvent(self.display)
        if not event:
          break
        self.signal(event)

  def signal(self, event):
    type, keycode, modifiers, value = event
    if self.handlers.has_key((keycode, modifiers)):
      self.handlers[(keycode, modifiers)]().value = value
    if self.handlers.has_key((keycode, Any)):
      self.handlers[(keycode, Any)]().value = value

  def key(self, keycode, modifiers = Any):
    name = (keycode, modifiers)
      
    if self.handlers.has_key(name):
      return self.handlers[name]()
    else:
      handler = InputSignal(0)
      grabkey.grabKey(self.display, keycode, modifiers, False)
      self.handlers[name] = ref(handler, lambda x: self.reset(keycode, modifiers))
      return handler
      
  def reset(self, keycode = None, modifiers = Any):
    if keycode is None:
      while len(self.handlers):
        key, handler = self.handlers.popitem()
        self.reset(key[0], key[1])
    else:
      grabkey.ungrabKey(self.display, keycode, modifiers)
      if self.handlers.has_key((keycode, modifiers)):
        del self.handlers[(keycode, modifiers)]
