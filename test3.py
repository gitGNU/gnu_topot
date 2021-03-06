import xkey
from joystick import Joystick
from xrobot import *
from transform import *
from topot import Topot
from midi import MidiInput, MidiOutput

t = Topot()

t.add(xkey.Keys())
t.add(XRobot(20))

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
t.add(Ticker(20))
t.add(Joystick("/dev/input/js0"), "j0_")
t.add(MidiInput())
t.add(MidiOutput())

t.connect("note", 48, t.get("j0_button",0))
t.connect("print", "note 48", t.get("note", 48))
t.connect("print", "escape:", t.get("key", 9))
t.connect("click", 1, t.get("j0_button", 4))
t.connect("click", 2, t.get("j0_button", 5))
t.connect("click", 3, t.get("j0_button", 6))
t.connect("mousemove", pair(transform(t.get("j0_axis", 2), ampMove),
                            transform(t.get("j0_axis", 3), ampMove)))
t.connect("key", 98, t.get("j0_axis", 4))
t.connect("print", primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.connect("note", 50, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))

"""
t.connect("print", "escape:", t.get("key", 9))
t.connect("mod", "special", sticky(t.get("key", 66)))
t.withModifiers(on=["special"])
t.connect("print", "special-a:", t.get("key", 38))
t.clearModifiers()
t.withModifiers(off=["special"])
t.connect("print", "non-special-a:", t.get("key", 38))
t.clearModifiers()

t.add(Joystick("/dev/input/js0"), "j0_")
t.add(MidiInput())
t.add(MidiOutput())

def ampMove(input):
  i = input * 2.5
  return i * i * i

t.connect("click", 1, t.get("j0_button", 0))
t.connect("click", 2, t.get("j0_button", 1))
t.connect("click", 3, t.get("j0_button", 2))
t.connect("mousemove", pair(transform(t.get("j0_axis", 0), ampMove),
                            transform(t.get("j0_axis", 1), ampMove)))
t.connect("note", 48, t.get("j0_button", 3))

t.connect("print", "escape:", t.get("key", 9))
t.connect("mod", "special", sticky(t.get("key", 66)))
t.withModifiers(on=["special"])
t.connect("print", "special-a:", t.get("key", 38))
t.clearModifiers()
t.withModifiers(off=["special"])
t.connect("print", "non-special-a:", t.get("key", 38))
t.clearModifiers()
"""

t.start()
