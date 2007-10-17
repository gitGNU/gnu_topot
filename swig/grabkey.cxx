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

#define ROOT(display) (RootWindow(display, DefaultScreen(display)))

PyObject* getEvent(Display* display) {
  XEvent event;
  Py_BEGIN_ALLOW_THREADS;
  XWindowEvent(display, ROOT(display), KeyPressMask|KeyReleaseMask, &event);
  Py_END_ALLOW_THREADS;
  return Py_BuildValue("(siii)", "key", event.xkey.keycode,
                       event.xkey.state, event.type == KeyPress);
}

PyObject* checkEvent(Display* display) {
  XEvent event;
  if (XCheckWindowEvent(display, ROOT(display), KeyPressMask|KeyReleaseMask, &event))
    return Py_BuildValue("(siii)", "key", event.xkey.keycode,
                         event.xkey.state, event.type == KeyPress);
  else
    return Py_None;
}

int grabKey(Display* display, int keycode, unsigned int modifiers, bool pass) {
  int val = XGrabKey(display, keycode, modifiers, ROOT(display), pass, GrabModeSync, GrabModeAsync);
  XFlush(display);
  return val;
}

int ungrabKey(Display* display, int keycode, unsigned int modifiers) {
  int val = XUngrabKey(display, keycode, modifiers, ROOT(display));
  XFlush(display);
  return val;
}
