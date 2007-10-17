from weakref import ref
from inspect import getargspec

# Cheapo alternative to the Trellis library. With the marked difference that signals do not

class InputSignal(object):
  def __init__(self, init):
    self._value = init
    self._clients = []
    self.stable = True

  def _setValue(self, value):
    if not (self.stable and self._value == value):
      self._value = value
      for client in self._clients:
        client()._update()

  def _getValue(self):
    return self._value

  value = property(_getValue, _setValue)

  def _register(self, client):
    self._clients.append(ref(client, lambda r: self._clients.remove(r)))

class OutputSignal(object):
  def __init__(self, action, *sources):
    self._sources = sources
    for source in sources:
      source._register(self)
    self.action = action

  def _update(self):
    self.action()

class Signal(InputSignal, OutputSignal):
  initialized = False
  _value = None
  
  def __init__(self, compute, *sources):
    expected, var, varkw, defs = getargspec(compute)
    if len(expected) == 0:
      compute_ = compute
    elif len(expected) == 1:
      compute_ = lambda: compute(self.value)
    else:
      compute_ = lambda: compute(self.value, self.initialized)
    def recompute():
      self.value = compute_()
    OutputSignal.__init__(self, recompute, *sources)
    InputSignal.__init__(self, compute_())
    self.initialized = True
