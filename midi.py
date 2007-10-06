from pyseq import *
from mqueue import MQueue
from weakref import WeakValueDictionary
from cell import *

# Completely untested.

class MidiInput(PySeq):
  def __init__(self, direct=False):
    PySeq.__init__(self, "topot")
    self.inport = self.createInPort('')
    self.notes = WeakValueDictionary()
    self.thread = MidiThread(self)

  def start(self, topot):
    self.topot = topot
    topot.registerInput("note", self.note)
    self.go = True
    self.thread.start()

  def stop():
    self.go = False

  def callback(self, event):
    if (self.direct):
      self.signal(event)
    else:
      self.topot.enqueue(self.signal, event)
    if self.go:
      return 1
    else:
      return 2

  def note(self, id):
    if self.notes.has_key(id):
      return self.notes[id]
    else:
      note = InputCell(0)
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
