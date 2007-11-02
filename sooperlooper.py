import xkey
from joystick import Joystick
from xrobot import *
from transform import *
from topot import Topot
from midi import MidiInput, MidiOutput

t = Topot()

t.add(xkey.Keys())
t.add(XRobot(20))
t.add(Ticker(20))
t.add(Joystick("/dev/input/js0"), "j0_")
t.add(MidiInput())
t.add(MidiOutput())


def ampMove(input):
  i = input * 4
  return i**3

def ampMoveDiscon(input):
  i = input * 2
  return i**3 * -1


class Printer:
  def start(self, topot):
    topot.registerOutput("print", self.printer)
  def printer(self, input, prefix = ""):
    def prnt():
      print prefix, input.value
    return OutputSignal(prnt, input)

t.add(Printer())

t.connect("key", 10, t.get("j0_button",0))
t.connect("key", 11, t.get("j0_button",1))
t.connect("key", 12, t.get("j0_button",2))
t.connect("key", 13, t.get("j0_button",3))
t.connect("key", 42, t.get("j0_button",4))
t.connect("key", 46, t.get("j0_button",5))
t.connect("key", 33, t.get("j0_button",6))
t.connect("key", 53, t.get("j0_button",7))

t.connect("mod", "cha1", t.get("j0_button", 0))
t.connect("mod", "cha2", t.get("j0_button", 1))
t.connect("mod", "cha3", t.get("j0_button", 2))
t.connect("mod", "cha4", t.get("j0_button", 3))

t.withModifiers(on=["cha1"])
t.connect("controller", 71, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.clearModifiers()
t.withModifiers(on=["cha2"])
t.connect("controller", 72, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.clearModifiers()
t.withModifiers(on=["cha3"])
t.connect("controller", 73, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.clearModifiers()
t.withModifiers(on=["cha4"])
t.connect("controller", 74, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.clearModifiers()






t.start()
