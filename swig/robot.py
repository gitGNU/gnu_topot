# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _robot

def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types



openDisplay = _robot.openDisplay

closeDisplay = _robot.closeDisplay

displayFD = _robot.displayFD

mousePos = _robot.mousePos

moveMouse = _robot.moveMouse

sendKeyEvent = _robot.sendKeyEvent

sendButtonEvent = _robot.sendButtonEvent
def setMouse(display, x, y):
  cx, cy = mousePos(display)
  moveMouse(display, x - cx, y - cy);


