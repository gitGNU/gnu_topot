%module robot

%{
#include <X11/Xlibint.h>
#undef _POSIX_C_SOURCE
%}

%inline %{
Display* openDisplay();
void closeDisplay(Display* display);
int displayFD(Display* display);

PyObject* mousePos(Display* display);
void moveMouse(Display* display, int dx, int dy);

void sendKeyEvent(Display* display, int keycode, int modifiers, int down);
void sendButtonEvent(Display* display, int button, int down);
%}

%pythoncode %{
def setMouse(display, x, y):
  cx, cy = mousePos(display)
  moveMouse(display, x - cx, y - cy);
%}
