#include <X11/Xlibint.h>
#undef _POSIX_C_SOURCE
#include <Python.h>

/* Simple C backend for grabbing and listening for X key events from
 * Python. Note the shameless use of global data everywhere. Should be
 * moved into some kind of object wrapper if you want to be able to
 * use more than one instance. The eventBlocker/getLastEvent trick is
 * designed to be used together with the 'listener' library, to
 * provide proper event callbacks -- as opposed to blocking the whole
 * Python process or polling for events.
 */

Display* display = NULL;
#define ROOT() (RootWindow(display, DefaultScreen(display)))
#define OPEN() if (display == NULL) open()

bool open() {
  if (display != NULL)
    return True;
  
  display = XOpenDisplay(0);
  if (display) {
    XSelectInput(display, ROOT(), KeyPressMask | KeyReleaseMask);
    return True;
  }
  else {
    return False;
  }
}

bool close() {
  if (display == NULL)
    return True;

  bool result = XCloseDisplay(display);
  display = NULL;
  return result;
}

bool isOpen() {
  return display != NULL;
}

PyObject* getEvent() {
  OPEN();
  XEvent event;
  Py_BEGIN_ALLOW_THREADS;
  XWindowEvent(display, ROOT(), KeyPressMask|KeyReleaseMask, &event);
  Py_END_ALLOW_THREADS;
  return Py_BuildValue("(siii)", "key", event.xkey.keycode,
                       event.xkey.state, event.type == KeyPress);
}

PyObject* checkEvent() {
  OPEN();
  XEvent event;
  if (XCheckWindowEvent(display, ROOT(), KeyPressMask|KeyReleaseMask, &event))
    return Py_BuildValue("(siii)", "key", event.xkey.keycode,
                         event.xkey.state, event.type == KeyPress);
  else
    return Py_None;
}

int grabKey(int keycode, unsigned int modifiers, bool pass) {
  OPEN();
  int val = XGrabKey(display, keycode, modifiers, ROOT(), pass, GrabModeSync, GrabModeAsync);
  XFlush(display);
  return val;
}

int ungrabKey(int keycode, unsigned int modifiers) {
  OPEN();
  int val = XUngrabKey(display, keycode, modifiers, ROOT());
  XFlush(display);
  return val;
}
