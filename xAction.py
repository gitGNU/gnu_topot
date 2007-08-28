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

from pyrobot import *
import JSW,sys,time
from pyseq import *

class XAction:
    def __init__(self):
        self.R = PyRobot()
        self.dev = "/dev/input/input6/js0"
        self.cal = "/tmp/.joystick"
        self.jsd = JSW.Joystick(self.dev,self.cal)
        self.ax = self.jsd.getAxisCoeff
        self.bt = self.jsd.getButtonState
        self.mouseX = 0
        self.mouseY = 0
        self.states = {}
        for i in range(self.jsd.axisCount):
            self.states['ax'+str(i)] = 0
        for i in range(self.jsd.buttonCount):
            self.states['bt'+str(i)] = 0
        self.states['ax4b'] = 0
        self.states['ax5b'] = 0
        for i in range(3):
            self.states['midi0'+str(i)] = 0

    def getMouseCoord(self):
        self.R.grabAll()
        ev = self.R.getEvent()
        dat = ev.getData()
        self.mouseX, self.mouseY = dat.x, dat.y
        self.R.releaseAll()

    def setMouseX(self, x, state):
        step = self.getMouseStep(x)
        if x > 0:
            self.mouseX += step + 1
            if self.mouseX > 1024: self.mouseX = 1024
        elif x < 0:
            self.mouseX += step - 1
            if self.mouseX < 0: self.mouseX = 0

    def setMouseY(self, y, state):
        step = self.getMouseStep(y)
        if y > 0:
            self.mouseY -= step + 1
            if self.mouseY > 768: self.mouseY = 768
        elif y < 0:
            self.mouseY -= step - 1
            if self.mouseY < 0: self.mouseY = 0

    def getMouseStep(self, s):
        return int(((round(s,2)*100)**3)/20000)

    def moveMouse(self):
        self.R.sendMotionEvent(self.mouseX, self.mouseY)

    def leftClick(self, click, state):
        if click == 1 and self.states[state] == 0:
            self.R.sendButtonEvent(1,1)
            self.states[state] = 1
        elif click == 0 and self.states[state] == 1:
            self.R.sendButtonEvent(1,0)
            self.states[state] = 0
    
    def rightClick(self, click, state):
        if click == 1 and self.states[state] == 0:
            self.R.sendButtonEvent(3,1)
            self.states[state] = 1
        elif click == 0 and self.states[state] == 1:
            self.R.sendButtonEvent(3,0)
            self.states[state] = 0

    def middleClick(self, click, state):
        if click == 1 and self.states[state] == 0:
            self.R.sendButtonEvent(2,1)
            self.states[state] = 1
        elif click == 0 and self.states[state] == 1:
            self.R.sendButtonEvent(2,0)
            self.states[state] = 0

    def arrowUpDownAx(self, click, state):
        if click == 1 and self.states[state] == 0:
            self.R.sendKeyEvent(98,1)
            self.states[state] = 1
        elif click == -1 and self.states[state+'b'] == 0:
            self.R.sendKeyEvent(104,1)
            self.states[state+'b'] = 1
        elif click == 0 and self.states[state] == 1:
            self.R.sendKeyEvent(98,0)
            self.states[state] = 0
        elif click == 0 and self.states[state+'b'] == 1:
            self.R.sendKeyEvent(104,0)
            self.states[state+'b'] = 0

    def arrowLeftRightAx(self, click, state):
        if click == 1 and self.states[state] == 0:
            self.R.sendKeyEvent(102,1)
            self.states[state] = 1
        elif click == -1 and self.states[state+'b'] == 0:
            self.R.sendKeyEvent(100,1)
            self.states[state+'b'] = 1
        elif click == 0 and self.states[state] == 1:
            self.R.sendKeyEvent(102,0)
            self.states[state] = 0
        elif click == 0 and self.states[state+'b'] == 1:
            self.R.sendKeyEvent(100,0)
            self.states[state+'b'] = 0

    def backspaceDeleteAx(self, click, state):
        if click == 1 and self.states[state] == 0:
            self.R.sendKeyEvent(107,1)
            self.states[state] = 1
        elif click == -1 and self.states[state+'b'] == 0:
            self.R.sendKeyEvent(22,1)
            self.states[state+'b'] = 1
        elif click == 0 and self.states[state] == 1:
            self.R.sendKeyEvent(107,0)
            self.states[state] = 0
        elif click == 0 and self.states[state+'b'] == 1:
            self.R.sendKeyEvent(22,0)
            self.states[state+'b'] = 0

    def enterEscapeAx(self, click, state):
        if click == 1 and self.states[state] == 0:
            self.R.sendKeyEvent(9,1)
            self.states[state] = 1
        elif click == -1 and self.states[state+'b'] == 0:
            self.R.sendKeyEvent(36,1)
            self.states[state+'b'] = 1
        elif click == 0 and self.states[state] == 1:
            self.R.sendKeyEvent(9,0)
            self.states[state] = 0
        elif click == 0 and self.states[state+'b'] == 1:
            self.R.sendKeyEvent(36,0)
            self.states[state+'b'] = 0
