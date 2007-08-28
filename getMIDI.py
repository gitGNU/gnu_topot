# Copyright 2007 'Marcell Mars' <ki.ber@kom.uni.st>
# 
# This file is part of Topot.
#
# Topot is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Topot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyseq import *
import xAction 

class GetMIDI(PySeq):
    def __init__(self):
        PySeq.__init__(self,'GetMIDI')
        self.iport = self.createInPort('')

    def startGetMIDI(self):
        self.mt=MidiThread(self)
        self.mt.start()

    def callback(self, ev):
        if ev.type == SND_SEQ_EVENT_NOTEON and ev.getData().note == 48 and ev.getData().velocity > 0:
            K.leftClick(1, 'midi00')
        if ev.type == SND_SEQ_EVENT_NOTEON and ev.getData().note == 48 and ev.getData().velocity == 0:
            K.leftClick(0, 'midi00')

        if ev.type == SND_SEQ_EVENT_NOTEON and ev.getData().note == 49 and ev.getData().velocity > 0:
            K.middleClick(1, 'midi01')
        if ev.type == SND_SEQ_EVENT_NOTEON and ev.getData().note == 49 and ev.getData().velocity == 0:
            K.middleClick(0, 'midi01')

        if ev.type == SND_SEQ_EVENT_NOTEON and ev.getData().note == 50 and ev.getData().velocity > 0:
            K.rightClick(1, 'midi02')
        if ev.type == SND_SEQ_EVENT_NOTEON and ev.getData().note == 50 and ev.getData().velocity == 0:
            K.rightClick(0, 'midi02')

        if ev.type == SND_SEQ_EVENT_CONTROLLER and ev.getData().param == 73:
            K.mouseX = (ev.getData().value + 1)*(1024/128)
            K.moveMouse()
        if ev.type == SND_SEQ_EVENT_CONTROLLER and ev.getData().param == 72:
            K.mouseY = (ev.getData().value + 1)*(1024/128)
            K.moveMouse()

        return 1

K = None

def run():
    global K, Midi
    K = XAction.XAction()
    Midi = GetMIDI()
    Midi.startGetMIDI()
