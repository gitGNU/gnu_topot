PYTHONPATH = /usr/include/python2.4/

all: _robot.so _grabkey.so _readjoy.so
	touch __init__.py

clean:
	rm -f *.so *.o *_wrap.cxx *.py *.pyc

%_wrap.cxx: %.i
	swig -c++ -python $<

%.o: %.cxx
	g++ -c -fPIC $< -I$(PYTHONPATH)

_robot.so: robot.o robot_wrap.o
	g++ -shared $^ -o $@ -lX11 -lXtst

_grabkey.so: grabkey.o grabkey_wrap.o
	g++ -shared $^ -o $@ -lX11

_readjoy.so: readjoy.o readjoy_wrap.o
	g++ -shared $^ -o $@
