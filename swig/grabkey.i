%module grabkey

%{
#include <X11/Xlibint.h>
#undef _POSIX_C_SOURCE
%}

#define ShiftMask		(1<<0)
#define LockMask		(1<<1)
#define ControlMask		(1<<2)
#define Mod1Mask		(1<<3)
#define Mod2Mask		(1<<4)
#define Mod3Mask		(1<<5)
#define Mod4Mask		(1<<6)
#define Mod5Mask		(1<<7)
#define AnyModifier		(1<<15)

%inline %{
PyObject* getEvent(Display* display);
PyObject* checkEvent(Display* display);

int grabKey(Display* display, int keycode, unsigned int modifiers, bool pass);
int ungrabKey(Display* display, int keycode, unsigned int modifiers);
%}
