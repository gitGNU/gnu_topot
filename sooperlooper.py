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

t.connect("key", 10, t.get("j0_button",0)) # after pressing first button on gamepad press 1 for the first loop
t.connect("key", 11, t.get("j0_button",1)) # press 2
t.connect("key", 12, t.get("j0_button",2)) # press 3
t.connect("key", 13, t.get("j0_button",3)) # press 4
t.connect("key", 42, t.get("j0_button",4)) # after pressing fifth button on gamepad press r for record selected loop 
t.connect("key", 46, t.get("j0_button",5)) # press o for overdub
t.connect("key", 33, t.get("j0_button",6)) # press p for replace
t.connect("key", 53, t.get("j0_button",7)) # press x for multiply


t.connect("mod", "cha1", t.get("j0_button", 0)) # setting up modifiers
t.connect("mod", "cha2", t.get("j0_button", 1)) #
t.connect("mod", "cha3", t.get("j0_button", 2)) #
t.connect("mod", "cha4", t.get("j0_button", 3)) #

t.withModifiers(on=["cha1"]) # while pressed first button move right axis for wet volume of the first loop
t.connect("controller", 71, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.clearModifiers()

t.withModifiers(on=["cha2"]) # while pressed second button move right axis for wet volume of the second loop
t.connect("controller", 72, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.clearModifiers()

t.withModifiers(on=["cha3"]) # while pressed third button move right axis for wet volume of the third loop
t.connect("controller", 73, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.clearModifiers()

t.withModifiers(on=["cha4"]) # while pressed forth button move right axis for wet volume of the forth loop
t.connect("controller", 74, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 127))
t.clearModifiers()

t.connect("key", 10, t.get("pgmchange", 1)) # after pressing first switch on fcb1010 press 1 for the first loop
t.connect("key", 11, t.get("pgmchange", 2)) # after pressing second switch on fcb1010 press 2 for the second loop
t.connect("key", 12, t.get("pgmchange", 6)) # after pressing sixth switch on fcb1010 press 3 for the third loop
t.connect("key", 13, t.get("pgmchange", 7)) # after pressing seventh switch on fcb1010 press 4 for the forth loop
t.connect("key", 42, t.get("pgmchange", 3)) # after pressing third switch on fcb1010 press r for record selected loop
t.connect("key", 46, t.get("pgmchange", 4)) # after pressing forth switch on fcb1010 press o for overdub selected loop
t.connect("key", 33, t.get("pgmchange", 5)) # after pressing fifth switch on fcb1010 press p for replace selected loop
t.connect("key", 53, t.get("pgmchange", 9)) # after pressing nineth switch on fcb1010 press x for multiply selected loop

t.start()
