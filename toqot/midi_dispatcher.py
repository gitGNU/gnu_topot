from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from pyalsa import alsaseq
import time

seq = alsaseq.Sequencer()
seq.create_simple_port("topot_reader", alsaseq.SEQ_PORT_TYPE_APPLICATION, alsaseq.SEQ_PORT_CAP_SUBS_WRITE | alsaseq.SEQ_PORT_CAP_WRITE)


class Bridge(QObject):
    def __init__(self, parent = None):
        super(Bridge, self).__init__(parent)
    def emitMessage(self, type, param, value):
        self.emit(SIGNAL("MIDI"), type, param, value)
        

class Midi(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.bridge = Bridge()
        self.counter = 0
        self.counter2 = 0
        #self.seq = alsaseq.Sequencer()
        self.evnt = {'type' : "", 'param': "", 'value' : ""}
        #self.seq.create_simple_port("topot_reader", alsaseq.SEQ_PORT_TYPE_APPLICATION, alsaseq.SEQ_PORT_CAP_SUBS_WRITE | alsaseq.SEQ_PORT_CAP_WRITE)
        
    def run(self):
        self.readMidi()
        self.exec_()
     
    def readMidi(self):
        while True:
          events = seq.receive_events(100)
          for event in events:
            if event.type == alsaseq.SEQ_EVENT_CONTROLLER :
              self.evnt['type'] = 'cc'
              self.evnt['param'] = event.get_data()['control.param']
              self.evnt['value'] = event.get_data()['control.value']
            elif event.type == alsaseq.SEQ_EVENT_NOTEON:
              self.evnt['type'] = 'note'
              self.evnt['param'] = event.get_data()['note.note']
              self.evnt['value'] = event.get_data()['note.velocity']
            elif event.type == alsaseq.SEQ_EVENT_PGMCHANGE:
              self.evnt['type'] = 'pc'
              self.evnt['param'] = event.get_data()['control.value']
              self.evnt['value'] = event.get_data()['control.value']
          
            self.bridge.emitMessage(str(self.evnt['type']), str(self.evnt['param']), str(self.evnt['value']))
          time.sleep(.0001)

midi = Midi()
'''test:

_ip.magic("run -i midi_dispatcher.py")

def foo(type, param, value):
      print "type: %s, param: %s, value: %s" % (type, param, value)
    
QObject.connect(midi.bridge, SIGNAL('MIDI'), foo)
midi.start()
'''
