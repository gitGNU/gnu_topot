# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _grabkey

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


ShiftMask = _grabkey.ShiftMask
LockMask = _grabkey.LockMask
ControlMask = _grabkey.ControlMask
Mod1Mask = _grabkey.Mod1Mask
Mod2Mask = _grabkey.Mod2Mask
Mod3Mask = _grabkey.Mod3Mask
Mod4Mask = _grabkey.Mod4Mask
Mod5Mask = _grabkey.Mod5Mask
AnyModifier = _grabkey.AnyModifier

getEvent = _grabkey.getEvent

checkEvent = _grabkey.checkEvent

grabKey = _grabkey.grabKey

ungrabKey = _grabkey.ungrabKey

