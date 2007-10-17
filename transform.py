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
