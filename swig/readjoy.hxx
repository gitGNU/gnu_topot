class Joystick {
public:
  Joystick(const char* device);
  ~Joystick();

  PyObject* getEvent();
  int nAxis();
  int nButtons();
private:
  int fd;
  char axis, buttons;
};
