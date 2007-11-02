# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _readjoy

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


class Joystick(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, Joystick, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, Joystick, name)
    def __repr__(self):
        return "<C Joystick instance at %s>" % (self.this,)
    def __init__(self, *args):
        _swig_setattr(self, Joystick, 'this', _readjoy.new_Joystick(*args))
        _swig_setattr(self, Joystick, 'thisown', 1)
    def __del__(self, destroy=_readjoy.delete_Joystick):
        try:
            if self.thisown: destroy(self)
        except: pass
    def getEvent(*args): return _readjoy.Joystick_getEvent(*args)
    def nAxis(*args): return _readjoy.Joystick_nAxis(*args)
    def nButtons(*args): return _readjoy.Joystick_nButtons(*args)
    def fileno(*args): return _readjoy.Joystick_fileno(*args)

class JoystickPtr(Joystick):
    def __init__(self, this):
        _swig_setattr(self, Joystick, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, Joystick, 'thisown', 0)
        _swig_setattr(self, Joystick,self.__class__,Joystick)
_readjoy.Joystick_swigregister(JoystickPtr)


