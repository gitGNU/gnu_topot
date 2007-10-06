import xkey
from joystick import Joystick
from xrobot import *
from mqueue import MQueue
from transform import *

q = MQueue()

def ampMove(input):
  i = input * 2.5
  return i * i * i

j = Joystick("/dev/input/js0", q)

xr = XRobot(pair(transform(j.axis[2], ampMove),
                 transform(j.axis[3], ampMove)),
            20) # move mouse at 20 Hz
xr.connectButton(j.button[0], 1)
xr.connectButton(j.button[1], 2)
xr.connectButton(j.button[2], 3)

xr.connectKey(j.button[3], 36)
xr.connectKey(j.button[4], 22)
xr.connectKey(j.button[6], 65)
xr.connectKey(j.button[7], 9)

k = xkey.Keys(q)
xr.connectKey(k.key(66), 23)

q.start()
