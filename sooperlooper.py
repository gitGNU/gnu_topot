import xkey
from joystick import Joystick
from xrobot import *
from transform import *
from topot import Topot
from midi import MidiInput, MidiOutput
from osc import OscOutput

def ampMove(input):
  i = input * 4
  return i**3

def ampMoveDiscon(input):
  i = input * 0.7
  return i**9 * -1

class Printer:
  def start(self, topot):
    topot.registerOutput("print", self.printer)
  def printer(self, input, prefix = ""):
    def prnt():
      print prefix, input.value
    return OutputSignal(prnt, input)


t = Topot()

t.add(xkey.Keys())
t.add(XRobot(20))
t.add(Ticker(20))
t.add(Joystick("/dev/input/js0"), "j0_")
t.add(MidiInput())
t.add(MidiOutput())
t.add(Printer())
t.add(OscOutput())

t.connect("print", "gamepad_button_0", t.get("j0_button", 0))
t.connect("print", "fcb1010_pgmchange_1", t.get("pgmchange", 1))

t.connect("osc", "/set", ["selected_loop_num", 2], "127.0.0.1", 9951, t.get("pgmchange", 0)) # after pressing first switch on fcb1010 select third loop 
t.connect("osc", "/set", ["selected_loop_num", 3], "127.0.0.1", 9951, t.get("pgmchange", 5)) # after pressing first switch on fcb1010 select forth loop 
t.connect("osc", "/set", ["selected_loop_num", 4], "127.0.0.1", 9951, t.get("pgmchange", 1)) # after pressing first switch on fcb1010 select fifth loop
t.connect("osc", "/set", ["selected_loop_num", 5], "127.0.0.1", 9951, t.get("pgmchange", 6)) # after pressing first switch on fcb1010 select sixth loop

t.connect("mod", "cha1", t.get("j0_button", 3)) # setting up modifiers
t.connect("mod", "cha2", t.get("j0_button", 0)) #
t.connect("mod", "cha3", t.get("j0_button", 2)) #
t.connect("mod", "cha4", t.get("j0_button", 1)) #

t.withModifiers(on=["cha1"]) # while pressed first button move right axis for wet volume of the first loop
t.connect("osc", "/sl/0/set", ["wet"], "127.0.0.1", 9951, True, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 1))
t.connect("osc", "/sl/0/hit", ["record"], "127.0.0.1", 9951, t.get("j0_button", 4))
t.connect("osc", "/sl/0/hit", ["overdub"], "127.0.0.1", 9951, t.get("j0_button", 5))
t.connect("osc", "/sl/0/hit", ["substitute"], "127.0.0.1", 9951, t.get("j0_button", 6))
t.connect("osc", "/sl/0/hit", ["multiply"], "127.0.0.1", 9951, t.get("j0_button", 7))
t.connect("osc", "/sl/0/hit", ["record"], "127.0.0.1", 9951, False, True, t.get("pgmchange", 3))
t.clearModifiers()

t.withModifiers(on=["cha2"]) # while pressed second button move right axis for wet volume of the second loop
t.connect("osc", "/sl/1/set", ["wet"], "127.0.0.1", 9951, True, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 1))
t.connect("osc", "/sl/1/hit", ["record"], "127.0.0.1", 9951, t.get("j0_button", 4))
t.connect("osc", "/sl/1/hit", ["overdub"], "127.0.0.1", 9951, t.get("j0_button", 5))
t.connect("osc", "/sl/1/hit", ["substitute"], "127.0.0.1", 9951, t.get("j0_button", 6))
t.connect("osc", "/sl/1/hit", ["multiply"], "127.0.0.1", 9951, t.get("j0_button", 7))
t.clearModifiers()

t.withModifiers(on=["cha3"]) # while pressed third button move right axis for wet volume of the third loop
t.connect("osc", "/sl/2/set", ["wet"], "127.0.0.1", 9951, True, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 1))
t.connect("osc", "/sl/2/hit", ["record"], "127.0.0.1", 9951, t.get("j0_button", 4))
t.connect("osc", "/sl/2/hit", ["overdub"], "127.0.0.1", 9951, t.get("j0_button", 5))
t.connect("osc", "/sl/2/hit", ["substitute"], "127.0.0.1", 9951, t.get("j0_button", 6))
t.connect("osc", "/sl/2/hit", ["multiply"], "127.0.0.1", 9951, t.get("j0_button", 7))
t.clearModifiers()

t.withModifiers(on=["cha4"]) # while pressed forth button move right axis for wet volume of the forth loop
t.connect("osc", "/sl/3/set", ["wet"], "127.0.0.1", 9951, True, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 1))
t.connect("osc", "/sl/3/hit", ["record"], "127.0.0.1", 9951, t.get("j0_button", 4))
t.connect("osc", "/sl/3/hit", ["overdub"], "127.0.0.1", 9951, t.get("j0_button", 5))
t.connect("osc", "/sl/3/hit", ["substitute"], "127.0.0.1", 9951, t.get("j0_button", 6))
t.connect("osc", "/sl/3/hit", ["multiply"], "127.0.0.1", 9951, t.get("j0_button", 7))
t.clearModifiers()

t.start()
