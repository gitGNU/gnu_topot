%module readjoy

%exception Joystick {
   try {
      $action
   } catch (std::runtime_error &e) {
      PyErr_SetString(PyExc_IOError, const_cast<char*>(e.what()));
      return NULL;
   }
}

%include readjoy.hxx

%{
#include "readjoy.hxx"
#include <stdexcept>
%}
