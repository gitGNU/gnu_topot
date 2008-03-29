import simpleosc
from signals import *

class OscOutput:
  def __init__(self):
    simpleosc.init()

  def start(self, topot):
    topot.registerOutput("osc", self.osc)

  def osc(self, source, oscpath, osccommand, ip, port, usesource = False, ignorekeydown = False):
    return OutputSignal(self.sendOsc(source, oscpath, osccommand, ip, port, usesource, ignorekeydown), source)

  def sendOsc(self, source, oscpath, osccommand, ip, port, usesource, ignorekeydown):
    def sendOscMsg():
      if usesource:
        osccommand.append(source.value)
        simpleosc.sendMsg(oscpath, osccommand, ip, port)
        osccommand.pop()
      elif ignorekeydown and source.value == 1:
        simpleosc.sendMsg(oscpath, osccommand, ip, port)
      else: 
        simpleosc.sendMsg(oscpath, osccommand, ip, port)

    return sendOscMsg
