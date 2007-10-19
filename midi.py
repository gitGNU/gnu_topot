from threading import Thread
from pyseq import *
from weakref import WeakValueDictionary
from signals import *
from Queue import Queue
import os

# Uses a thread that fetches midi events, a queue to store these
# events, and a pipe for the main thread to select on. When an event
# is found, a single character is sent to the pipe, which causes the
# thing to unblock, so that the run method can read that character,
# fetch the event from the queue, and dispatch it.

class MidiInput(PySeq):
  def __init__(self):
    PySeq.__init__(self, "topot_midi_in")
    self.inport = self.createInPort('')
    self.notes = WeakValueDictionary()
    self.queue = Queue()
    self.pin, self.pout = os.pipe()
    self.thread = MidiThread(self)

  def start(self, topot):
    topot.registerInput("note", self.note)
    self.thread.start()
    return self.run()

  def callback(self, event):
    self.queue.put(event)
    os.write(self.pout, "!")

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

  def signal(self, event):
    def sendNote(note, value):
      if self.notes.has_key(note):
        self.notes[note].value = value

    data = event.getData()
    if event.type == SND_SEQ_EVENT_NOTEON:
      sendNote(data.note, data.velocity)
    elif event.type == SND_SEQ_EVENT_NOTEOFF:
      sendNote(data.note, 0)

class MidiOutput(PySeq):
  def __init__(self):
    PySeq.__init__(self, "topot_midi_out")
    self.out = self.createOutPort()

  def start(self, topot):
    topot.registerOutput("note", self.note)
    topot.registerOutput("controller", self.controller)

  def controller(self, source, control, channel=0):
    setController = lambda e: e.setController(channel, control, int(source.value))
    return OutputSignal(self.sendEvent(setController), source)

  def note(self, source, id, channel=0):
    setNote = lambda e: e.setNoteOn(channel, id, int(source.value))
    return OutputSignal(self.sendEvent(setNote), source)

  def sendEvent(self, modify):
    def sendNote():
      event = snd_seq_event()
      modify(event)
      event.setSource(0)
      event.setSubscribers()
      event.sendNow(self, self.out)
    return sendNote
