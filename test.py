import xkey
from joystick import Joystick
from xrobot import *
from transform import *
from topot import Topot

t = Topot()

t.add(xkey.Keys())
t.add(XRobot(20))
t.add(Joystick("/dev/input/js0"), "j0_")

def ampMove(input):
  i = input * 2.5
  return i * i * i

t.connect("click", 1, t.get("j0_button", 0))
t.connect("click", 2, t.get("j0_button", 1))
t.connect("click", 3, t.get("j0_button", 2))
t.connect("mousemove", pair(transform(t.get("j0_axis", 0), ampMove),
                            transform(t.get("j0_axis", 1), ampMove)))

t.start()
