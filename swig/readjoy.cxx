#include <stdio.h>
#include <unistd.h>
#include <string>
#include <stdexcept>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <linux/joystick.h>
#undef _POSIX_C_SOURCE
#include <Python.h>

#include "readjoy.hxx"

Joystick::Joystick(const char* device) {
  fd = open(device, O_RDONLY);
  if (fd == -1)
    throw std::runtime_error("Could not open joystick device.");

  ioctl(fd, JSIOCGAXES, &axis);
  ioctl(fd, JSIOCGBUTTONS, &buttons);
}

Joystick::~Joystick() {
  close(fd);
}

float asFloat(int value) {
  return static_cast<float>(value) / 32767;
}

PyObject* Joystick::getEvent() {
  js_event event;
  while (1) {
    Py_BEGIN_ALLOW_THREADS;
    read(fd, &event, sizeof(js_event));
    Py_END_ALLOW_THREADS;
    switch (event.type & ~JS_EVENT_INIT) {
    case JS_EVENT_AXIS:
      return Py_BuildValue("(sif)", "axis", event.number, asFloat(event.value));
    case JS_EVENT_BUTTON:
      return Py_BuildValue("(sii)", "button", event.number, event.value);
    }
  }
}

int Joystick::nAxis() {
  return axis;
}
int Joystick::nButtons() {
  return buttons;
}
