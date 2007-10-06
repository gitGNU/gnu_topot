from swig import readjoy
from cell import *
from threading import Thread

class Joystick(Thread):
  go = True
  
  def __init__(self, device, queue):
    Thread.__init__(self)
    self.setDaemon(True)
    self.reader = readjoy.Joystick(device)
    self.queue = queue
    self.button = [InputCell(False) for x in range(self.reader.nButtons())]
    self.axis = [InputCell(0) for x in range(self.reader.nAxis())]
    self.start()

  def run(self):
    while self.go:
      self.queue.send(self, self.reader.getEvent())

  def signal(self, event):
    type, number, value = event
    if type == "button":
      self.button[number].value = value
    elif type == "axis":
      self.axis[number].value = value

  def stop():
    self.reader = None
    self.go = False
