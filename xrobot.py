from swig import robot
from signals import *
from threading import Thread
import time

class XRobot(Thread):
  def __init__(self, frequency = 20):
    Thread.__init__(self)
    self.setDaemon(True)
    self.display = robot.openDisplay()
    self.move_display = None
    self.motion = None
    self.delay = 1.0 / frequency

  def __del__(self):
    if self.move_display:
      robot.closeDisplay(self.move_display)
    robot.closeDisplay(self.display)

  def start(self, topot):
    self.topot = topot
    topot.registerOutput("key", self.connectKey)
    topot.registerOutput("click", self.connectButton)
    topot.registerOutput("mousemove", self.connectMotion)
    Thread.start(self)

  def run(self):
    self.move_display = robot.openDisplay()
    while True:
      dx, dy = (self.motion and self.motion.value) or (0, 0)
      if dx or dy:
        robot.moveMouse(self.move_display, int(dx), int(dy))
      time.sleep(self.delay)

  def connectMotion(self, input):
    self.motion = input
    return input

  def connectButton(self, input, button):
    def sendButton():
      robot.sendButtonEvent(self.display, button, int(input.value))
    return OutputSignal(sendButton, input)
      
  def connectKey(self, input, keycode, modifiers = 0):
    def sendKey():
      robot.sendKeyEvent(self.display, keycode, modifiers, int(input.value))
    return OutputSignal(sendKey, input)

  def disconnect(self, signal):
    self.connected.remove(signal)
