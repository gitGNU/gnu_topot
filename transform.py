from signals import *
from threading import Thread

def amplify(signal, factor):
  return Signal(lambda: signal.value * factor, signal)

def pair(a, b):
  return Signal(lambda: (a.value, b.value), a, b)

def transform(signal, f):
  return Signal(lambda: f(signal.value), signal)

def sticky(signal):
  state = [False]
  def flip():
    if signal.value:
      state[0] = not state[0]
    return state[0]
  return Signal(flip, signal)

def primitive(signal, initstate = 0, minval = None, maxval = None):
  def limit(value):
    if not minval is None:
      value = max(minval, value)
    if not maxval is None:
      value = min(maxval, value)
    return value

  def change(value):
    return limit(value + signal.value)
  return Signal(change, signal, init = initstate)
      
class Ticker:
  def __init__(self, frequency):
    self.frequency = frequency
    self.signal = InputSignal(False)

  def start(self, topot):
    topot.registerInput("tick", lambda : self.signal)
    return self.tick()
  def tick(self):
    while True:
      yield ("wait", 1.0/self.frequency)
      self.signal.value = not self.signal.value

def repeat(ticks, signal):
  result = Signal(lambda : signal.value, ticks)
  result.stable = False
  return result
