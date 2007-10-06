from swig import robot
from cell import *
from threading import Thread
import time

class XRobot(Thread):
  move_display = None
  
  def __init__(self, motion, frequency = 20):
    Thread.__init__(self)
    self.setDaemon(True)
    if motion:
      self.motion = motion
      self.delay = 1.0 / frequency
      self.move_display = robot.openDisplay()
      self.start()
    self.display = robot.openDisplay()
    self.connected = []

  def __del__(self):
    if self.move_display:
      robot.closeDisplay(self.move_display)
    robot.closeDisplay(self.display)

  def run(self):
    while True:
      dx, dy = self.motion.value
      if dx or dy:
        robot.moveMouse(self.move_display, int(dx), int(dy))
      time.sleep(self.delay)

  def connectButton(self, input, button):
    def sendButton():
      robot.sendButtonEvent(self.display, button, int(input.value))
    cell = OutputCell(sendButton, input)
    self.connected.append(cell)
    return cell
      
  def connectKey(self, input, keycode, modifiers = 0):
    def sendKey():
      robot.sendKeyEvent(self.display, keycode, modifiers, int(input.value))
    cell = OutputCell(sendKey, input)
    self.connected.append(cell)
    return cell

  def disconnect(self, cell):
    self.connected.remove(cell)
