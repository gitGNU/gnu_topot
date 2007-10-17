from swig import readjoy
from signals import *

class Joystick:
  def __init__(self, device):
    self.reader = readjoy.Joystick(device)
    self.button = [InputSignal(False) for x in range(self.reader.nButtons())]
    self.axis = [InputSignal(0) for x in range(self.reader.nAxis())]

  def start(self, topot):
    topot.registerInput("button", lambda b: self.button[b])
    topot.registerInput("axis", lambda a: self.axis[a])
    return self.run()

  def run(self):
    while True:
      yield("in", self.reader)
      self.signal(self.reader.getEvent())

  def signal(self, event):
    type, number, value = event
    if type == "button":
      self.button[number].value = value
    elif type == "axis":
      self.axis[number].value = value
