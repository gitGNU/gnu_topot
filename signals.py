# Cheapo alternative to the Trellis library. With the marked
# difference that signals do not automatically fire when they are
# created, and that you manually have to specify dependencies, which
# means it works a little less automagical, but you do have more
# control over dependencies.

# Signals hold values, which they compute based on the values of other
# signals. Changes to these values are automatically propagated. The
# dependencies between signal objects are supposed to form non-cyclic
# graphs. If you make a cycle, you have an infinite loop.

from weakref import ref
from inspect import getargspec


# Use this class for signals at the start of the chain. These are not
# dependant on other signals, and get their value by direct
# assignment to their value property.
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


# Use this class for signals at the end of the chain. No signals can
# depend on these, and they affect the outside world (though their
# action function) rather than computing a value.
class OutputSignal(object):
  def __init__(self, action, *sources):
    self._sources = sources
    for source in sources:
      source._register(self)
    self.action = action

  def _update(self):
    self.action()


# Regular signal class. The constructor expects a function that
# recomputes the signal's value and any number of dependencies as
# arguments. This function can take 0, 1, or 2 arguments. If it takes
# at least one, its first argument will be the previous value of the
# signal. If it takes two, its second argument is a boolean indicating
# whether the signal has been initialized yet.
class Signal(InputSignal, OutputSignal):
  _value = None
  
  def __init__(self, compute, *sources):
    expected, var, varkw, defs = getargspec(compute)
    initialized = False
    if len(expected) == 0:
      compute_ = compute
    elif len(expected) == 1:
      compute_ = lambda: compute(self.value)
    else:
      compute_ = lambda: compute(self.value, initialized)
    def recompute():
      self.value = compute_()
    OutputSignal.__init__(self, recompute, *sources)
    InputSignal.__init__(self, compute_())
    initialized = True
