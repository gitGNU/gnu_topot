import xkey
from joystick import Joystick
from xrobot import *
from transform import *
from topot import Topot
from midi import MidiInput, MidiOutput
from osc import OscOutput 
from var import VarOutput

def ampMove(input):
  i = input * 4
  return i**3

def ampMoveDiscon(input):
  i = input * 0.7
  return i**9 * -1

class Printer:
  def start(self, topot):
    topot.registerOutput("print", self.printer)
  def printer(self, input, prefix = "print: "):
    def prnt():
      #print "print: " + str(input.__dict__)
      print prefix, input.value
    return OutputSignal(prnt, input)

class Foo:
  def __init__(self):
    self.foo = ""

f = Foo()

t = Topot()

t.add(xkey.Keys())
t.add(XRobot(20))

t.add(Ticker(20))
t.add(Joystick("/dev/input/js0"), "j0_")

t.add(Printer())
t.add(MidiInput())
t.add(MidiOutput())
t.add(OscOutput())
#t.add(VarOutput())

t.connect("print", "gamepad_button_0", t.get("j0_button", 0))
t.connect("print", "fcb1010_pgmchange_0", t.get("pgmchange", 0))
t.connect("print", "fcb1010_pgmchange_1", t.get("pgmchange", 1))
t.connect("print", "fcb1010_pgmchange_2", t.get("pgmchange", 2))
t.connect("print", "fcb1010_pgmchange_3", t.get("pgmchange", 3))
t.connect("print", "fcb1010_pgmchange_4", t.get("pgmchange", 4))
t.connect("print", "fcb1010_pgmchange_5", t.get("pgmchange", 5))
t.connect("print", "fcb1010_pgmchange_6", t.get("pgmchange", 6))
t.connect("print", "fcb1010_pgmchange_7", t.get("pgmchange", 7))
t.connect("print", "fcb1010_pgmchange_8", t.get("pgmchange", 8))

"""
t.connect('var', '3', f.foo, t.get("key", 66))
t.connect('var', '4', f.foo, t.get("key", 23))
t.connect('var', '5', f.foo, t.get("key", 9))
t.connect('print', "foo: "+ f.foo, t.get("key", 23))
t.connect('print', f.foo, t.get("key", 66))
t.connect('print', f.foo, t.get("key", 9))
print "test: " + str(id(t))

t.add(Joystick("/dev/input/js0"), "j0_")
t.add(MidiInput())
t.add(MidiOutput())

def ampMove(input):
  i = input * 2.5
  return i * i * i

t.connect("pgmchange", 39, t.get("key", 9))
t.connect("print", "Print Controller: ", t.get("controller", 27))
t.connect("print", "Print PgmChange2: ", t.get("pgmchange", 2))
t.connect("print", "Print PgmChange3: ", t.get("pgmchange", 3))
t.connect("print", "Print PgmChange4: ", t.get("pgmchange", 4))
t.connect("print", "Print note: ", t.get("note", 49))
t.connect("print", "key escape: ", t.get("key", 9))
t.connect("osc", "/sl/0/hit", ["record"], "127.0.0.1", 9951, t.get("key", 9)) 
t.connect("osc", "/sl/0/set", ["wet"], "127.0.0.1", 9951, True, primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 1))
t.connect("print", "j0_axis_1: ", primitive(repeat(t.get("tick"), transform(t.get("j0_axis", 1), ampMoveDiscon)), 0, 0, 1))



t.connect("print", "escape:", t.get("key", 9))
t.connect("mod", "special", sticky(t.get("key", 66)))
t.withModifiers(on=["special"])
t.connect("print", "special-a:", t.get("key", 38))
t.clearModifiers()
t.withModifiers(off=["special"])
t.connect("print", "non-special-a:", t.get("key", 38))
t.clearModifiers()


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
