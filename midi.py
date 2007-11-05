from threading import Thread
from pyseq import *
from weakref import WeakValueDictionary
from signals import *
from Queue import Queue
import os
import random

# Uses a thread that fetches midi events, a queue to store these
# events, and a pipe for the main thread to select on. When an event
# is found, a single character is sent to the pipe, which causes the
# thing to unblock, so that the run method can read that character,
# fetch the event from the rueue, and dispatch it.

class MidiInput(PySeq):
  def __init__(self):
    PySeq.__init__(self, "topot_midi_in")
    self.inport = self.createInPort('')
    self.notes = WeakValueDictionary()
    self.controllers = WeakValueDictionary()
    self.pgmchanges = WeakValueDictionary()
    self.queue = Queue()
    self.pin, self.pout = os.pipe()
    self.thread = MidiThread(self)

  def start(self, topot):
    topot.registerInput("note", self.note)
    topot.registerInput("controller", self.controller)
    topot.registerInput("pgmchange", self.pgmchange)
    self.thread.start()
    return self.run()

  def callback(self, event):
    self.queue.put(event)
    os.write(self.pout, "!")
    return 1

  def run(self):
    while True:
      yield ("in", self.pin)
      os.read(self.pin, 1)
      self.signal(self.queue.get(True))
      
  def note(self, id):
    if self.notes.has_key(id):
      return self.notes[id]
    else:
      note = InputSignal(0)
      self.notes[id] = note
      return note

  def controller(self, id):
    if self.controllers.has_key(id):
      return self.controllers[id]
    else:
      controller = InputSignal(0)
      self.controllers[id] = controller
      return controller

  def pgmchange(self, id):
    if self.pgmchanges.has_key(id):
      return self.pgmchanges[id]
    else:
      pgmchange = InputSignal(0)
      self.pgmchanges[id] = pgmchange
      return pgmchange

  def signal(self, event):
    def sendNote(note, value):
      if self.notes.has_key(note):
        self.notes[note].value = value
  
    def sendController(controller, value):
      if self.controllers.has_key(controller):
	self.controllers[controller].value = value
    
    def sendPgmChange(pgmchange, value):
      if self.pgmchanges.has_key(pgmchange):
	self.pgmchanges[pgmchange].value = value

    data = event.getData()
    if event.type == SND_SEQ_EVENT_NOTEON:
      sendNote(data.note, data.velocity)
    elif event.type == SND_SEQ_EVENT_NOTEOFF:
      sendNote(data.note, 0)
    elif event.type == SND_SEQ_EVENT_CONTROLLER:
      sendController(data.param, data.value)
    elif event.type == SND_SEQ_EVENT_PGMCHANGE:
      sendPgmChange(data.value, random.randint(0,1000))	# randomize values so pgmchange will be fired up
      							# coz it doesn't fire it up if value didn't change
      
class MidiOutput(PySeq):
  def __init__(self):
    PySeq.__init__(self, "topot_midi_out")
    self.out = self.createOutPort()

  def start(self, topot):
    topot.registerOutput("note", self.note)
    topot.registerOutput("controller", self.controller)
    topot.registerOutput("pgmchange", self.pgmchange)

  def controller(self, source, control, channel=0):
    setController = lambda e: e.setController(channel, control, int(source.value))
    return OutputSignal(self.sendEvent(setController), source)

  def note(self, source, id, channel=0):
    setNote = lambda e: e.setNoteOn(channel, id, int(source.value))
    return OutputSignal(self.sendEvent(setNote), source)

  def pgmchange(self, source, pc, channel=0):
    setPgmChange = lambda e: e.setPgmChange(channel, pc)
    return OutputSignal(self.sendEvent(setPgmChange), source)
  
  def sendEvent(self, modify):
    def sendNote():
      event = snd_seq_event()
      modify(event)
      event.setSource(0)
      event.setSubscribers()
      event.sendNow(self, self.out)
    return sendNote
