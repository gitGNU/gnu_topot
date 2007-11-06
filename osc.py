import simpleosc
from signals import *

class OscOutput:
  def __init__(self):
    simpleosc.init()

  def start(self, topot):
    topot.registerOutput("osc", self.osc)

  def osc(self, source, oscpath, osccommand, ip, port, usesource=False):
    return OutputSignal(self.sendOsc(source, oscpath, osccommand, ip, port, usesource), source)

  def sendOsc(self, source, oscpath, osccommand, ip, port, usesource):
    def sendOscMsg():
      if usesource:
        osccommand.append(source.value)
        simpleosc.sendMsg(oscpath, osccommand, ip, port)
        osccommand.pop()
      simpleosc.sendMsg(oscpath, osccommand, ip, port)
    return sendOscMsg
