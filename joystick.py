from swig import readjoy
from cell import *
from threading import Thread

class Joystick(Thread):
  go = True
  
  def __init__(self, device):
    Thread.__init__(self)
    self.setDaemon(True)
    self.reader = readjoy.Joystick(device)
    self.button = [InputCell(False) for x in range(self.reader.nButtons())]
    self.axis = [InputCell(0) for x in range(self.reader.nAxis())]

  def start(self, topot):
    self.topot = topot
    topot.registerInput("button", lambda b: self.button[b])
    topot.registerInput("axis", lambda a: self.axis[a])
    Thread.start(self)

  def run(self):
    while self.go:
      self.topot.enqueue(self.signal, self.reader.getEvent())

  def signal(self, event):
    type, number, value = event
    if type == "button":
      self.button[number].value = value
    elif type == "axis":
      self.axis[number].value = value

  def stop():
    self.reader = None
    self.go = False
