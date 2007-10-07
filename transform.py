from cell import *
from threading import Thread

def amplify(cell, factor):
  return Cell(lambda: cell.value * factor, cell)

def pair(a, b):
  return Cell(lambda: (a.value, b.value), a, b)

def transform(cell, f):
  return Cell(lambda: f(cell.value), cell)

def sticky(cell):
  state = [False]
  def flip():
    if cell.value:
      state[0] = not state[0]
    return state[0]
  return Cell(flip, cell)
