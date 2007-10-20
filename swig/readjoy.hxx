class Joystick {
public:
  Joystick(const char* device);
  ~Joystick();

  PyObject* getEvent();
  int nAxis();
  int nButtons();
  int fileno();
  
private:
  int fd;
  char axis, buttons;
};
