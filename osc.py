import simpleosc
from signals import *

class OscOutput:
  def __init__(self):
    simpleosc.init()

  def start(self, topot):
    topot.registerOutput("osc", self.osc)

  def osc(self, source, oscpath, osccommand, ip, port, usesource=False, engine="sooperlooper"):
    if usesource:
      return OutputSignal(self.sendOsc(oscpath, (osccommand, source.value), ip, port), source)
    else:
        return OutputSignal(self.sendOsc(source, oscpath, osccommand, ip, port), source)


  def sendOsc(self, source, oscpath, osccommand, ip, port):
    def sendOscMsg():
      if source.value == 1:
        simpleosc.sendMsg(oscpath, osccommand, ip, port)
      else:
        pass
    return sendOscMsg
