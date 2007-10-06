#include <X11/Xlibint.h>
#include <X11/extensions/XTest.h>
#undef _POSIX_C_SOURCE
#include <Python.h>

// (note double evaluation)
#define ROOT(display) (RootWindow(display, DefaultScreen(display)))

Display* openDisplay() {
  Display* display = XOpenDisplay(0);
  if (display == NULL)
    PyErr_SetString(PyExc_IOError, "Could not open X display.");
  return display;
}

void closeDisplay(Display* display) {
  if (!XCloseDisplay(display))
    PyErr_SetString(PyExc_IOError, "Could not close X display.");
}

void moveMouse(Display* display, int dx, int dy) {
  if (!XWarpPointer(display, ROOT(display), None, 0, 0, 0, 0, dx, dy))
    PyErr_SetString(PyExc_IOError, "Moving mouse failed.");
  XFlush(display);
}

void getMousePos(Display* display, int& root_x, int& root_y,
                 int& child_x, int& child_y, unsigned int& modifiers) {
  Window root, child;
  XQueryPointer(display, ROOT(display), &root, &child, &root_x, &root_y,
                &child_x, &child_y, &modifiers);
}

PyObject* mousePos(Display* display) {
  int root_x, root_y, child_x, child_y;
  unsigned int modifiers;
  getMousePos(display, root_x, root_y, child_x, child_y, modifiers);
  return Py_BuildValue("(ii)", root_x, root_y);
}

/*
void sendKeyEvent(Display* display, int keycode, int modifiers, int down) {
  Window root = ROOT(display);
  XKeyEvent key;
  key.type = down ? KeyPress : KeyRelease;
  key.display = display;
  key.window = root;
  key.root = root;
  key.subwindow = None;
  key.time = CurrentTime;
  key.x = key.y = key.x_root = key.y_root = 0;
  key.state = modifiers;
  key.keycode = keycode;
  key.same_screen = true;
  if (!XSendEvent(display, InputFocus, true, 0, reinterpret_cast<XEvent*>(&key)))
    PyErr_SetString(PyExc_IOError, "Sending key event failed.");
  XFlush(display);
}

void sendButtonEvent(Display* display, int button, int down) {
  Window root = ROOT(display);
  XButtonEvent event;
  event.type = down ? ButtonPress : ButtonRelease;
  event.display = display;
  event.window = root;
  event.root = root;
  event.subwindow = None;
  event.time = CurrentTime;
  getMousePos(display, event.x_root, event.y_root, event.x, event.y, event.state);
  event.button = Button1;
  event.same_screen = true;
  if (!XSendEvent(display, InputFocus, true, 0, reinterpret_cast<XEvent*>(&event)))
    PyErr_SetString(PyExc_IOError, "Sending button event failed.");
  XFlush(display);
}
*/

// the plain-Xlib way doesn't seem to work, so we use XTest (which is,
// unfortunately, also flaky)

void sendKeyEvent(Display* display, int keycode, int modifiers, int down) {
  XTestFakeKeyEvent(display, keycode, down, 0);
  XFlush(display);
}

void sendButtonEvent(Display* display, int button, int down) {
  XTestFakeButtonEvent(display, button, down, 0);
  XFlush(display);
}
