import pyseq
import time

LSTART = (0,0,0)
LEND = (2,0,0)
MIDICLOCK = True


seq = pyseq.PySeq('topot_midi_out')
seq.createOutPort()
kju = pyseq.Queue(seq)
bpm = 30
tpq = 24
kju.setTempo(bpm, tpq)

class MidiInput(pyseq.PySeq):
  def __init__(self):
    pyseq.PySeq.__init__(self, "topot_midi_in")

    self.input = self.createInPort('')
    self.thread = pyseq.MidiThread(self)

  def callback(self, event):
    #print "tick: %s __ %s" % (str(kju.getTick()), str(event))
    processIncomingMidi(event)
    return 1


def tick2mbt(curpos):
  m, crr = divmod(curpos, 96)
  b, t = divmod(crr, 24)
  #print str("%3d:%3d:%3d" % (m, b, t)).replace(" ", "0")
  return m, b, t

def mbt2tick((m, b, t)):
  tick = t + b * 24 + m * 96
  return tick

def processIncomingMidi(event):
  if event.type == pyseq.SND_SEQ_EVENT_ECHO:
    populateNextTurn()

def populateNextTurn():
  for ev in evlist:
    ev.nposition = ev.position + ((divmod(kju.getTick(), mbt2tick(LEND))[0] + 1) * (mbt2tick(LEND) - mbt2tick(LSTART)))
    ev.schedule(kju, ev.nposition)
    ev.sendAsIs(seq)

mreceiver = MidiInput()
mreceiver.thread.start()

evlist = []

if MIDICLOCK:
  midistart = pyseq.snd_seq_event()
  midistart.type = pyseq.SND_SEQ_EVENT_START
  midistart.setSource(0)
  midistart.setSubscribers()
  midistart.position = 0
  midistart.schedule(kju, midistart.position)
  midistart.sendAsIs(seq)
  evlist.append(midistart)
  for i in range(mbt2tick(LSTART) +1, mbt2tick(LEND)):
    midiclock = pyseq.snd_seq_event()
    midiclock.type = pyseq.SND_SEQ_EVENT_CLOCK
    midiclock.setSource(0)
    midiclock.setSubscribers()
    midiclock.position = i
    midiclock.schedule(kju, midiclock.position)
    midiclock.sendAsIs(seq)
    evlist.append(midiclock)

echo = pyseq.snd_seq_event()
echo.type = pyseq.SND_SEQ_EVENT_ECHO
echo.setSource(0)
echo.setSubscribers()
echo.position = mbt2tick(LEND) - 1
echo.schedule(kju, echo.position) 
echo.sendAsIs(seq)
evlist.append(echo)

"""
drum = pyseq.snd_seq_event()
drum.setSource(0)
drum.setSubscribers()
drum.setNoteOn(0, 49, 120)
drum.position = mbt2tick((0,0,0))
drum.schedule(kju, drum.position)
drum.sendAsIs(seq)
evlist.append(drum)

drumoff = pyseq.snd_seq_event()
drumoff.setSource(0)
drumoff.setSubscribers()
drumoff.setNoteOff(0, 49, 0)
drumoff.position = mbt2tick((1,0,0))
drumoff.schedule(kju, drumoff.position)
drumoff.sendAsIs(seq)
evlist.append(drumoff)

nt = pyseq.snd_seq_event()
nt.setSource(0)
nt.setSubscribers()
nt.setNote(1, 49, 120, 96)
nt.position = mbt2tick((1,0,0))
nt.schedule(kju, nt.position)
nt.sendAsIs(seq)
evlist.append(nt)
"""
