import math

#from sooperlooper_qt import *
#from osc_server import *
#from myLogger import *

class MySooperLooperWidget(QObject):
  def __init__(self, parent = None):
    super(MySooperLooperWidget, self).__init__(parent)

    self.myScene = MainForm()
    self.myCycleTime = []
    self.myLoopCycles = []
    self.myLoopVelocity = []
    self.myLoopPlay = []
    self.myLoopRecord = []
    self.myLoopOverdub = []
    self.myLoopReplace = []
    self.myLoopSubstitute = []
    self.myLoopInsert = []
    self.myLoopMultiply = []
    self.myWidgetGroup = []
    self.loops = []
    self.currentstate = []

  def makeLoop(self, loop):
    self.loops.append(loop)
    self.emit(SIGNAL('makeloop'), loop)

    self.currentstate.append(loop)
    self.currentstate[loop] = mySooperLooperWidget.myLoopPlay

    self.myCycleTime.append(loop)
    self.myCycleTime[loop] = CycleTime()
    self.myCycleTime[loop].setZValue(0)
    self.myScene.scene.addItem(self.myCycleTime[loop])
    
    self.myLoopCycles.append(loop)
    self.myLoopCycles[loop] = LoopCycles()
    self.myLoopCycles[loop].setPos(15, 15)
    self.myLoopCycles[loop].setZValue(1)
    self.myScene.scene.addItem(self.myLoopCycles[loop])
    
    self.myLoopVelocity.append(loop)
    self.myLoopVelocity[loop] = LoopVelocity()
    self.myLoopVelocity[loop].setPos(24, 24)
    self.myLoopVelocity[loop].setZValue(2)
    self.myScene.scene.addItem(self.myLoopVelocity[loop])

    self.myLoopPlay.append(loop)
    self.myLoopPlay[loop] = LoopPlay()
    self.myLoopPlay[loop].setPos(30, 30)
    self.myLoopPlay[loop].setZValue(3)
    self.myScene.scene.addItem(self.myLoopPlay[loop])

    self.myLoopRecord.append(loop)
    self.myLoopRecord[loop] = LoopRecord()
    self.myLoopRecord[loop].setPos(30, 30)
    self.myLoopRecord[loop].setZValue(3)
    self.myLoopRecord[loop].hide()
    self.myScene.scene.addItem(self.myLoopRecord[loop])
    
    self.myLoopOverdub.append(loop)
    self.myLoopOverdub[loop] = LoopOverdub()
    self.myLoopOverdub[loop].setPos(30,30)
    self.myLoopOverdub[loop].setZValue(3)
    self.myLoopOverdub[loop].hide()
    self.myScene.scene.addItem(self.myLoopOverdub[loop])
    
    self.myLoopReplace.append(loop)
    self.myLoopReplace[loop] = LoopReplace()
    self.myLoopReplace[loop].setPos(30,30)
    self.myLoopReplace[loop].setZValue(3)
    self.myLoopReplace[loop].hide()
    self.myScene.scene.addItem(self.myLoopReplace[loop])
    
    self.myLoopSubstitute.append(loop)
    self.myLoopSubstitute[loop] = LoopSubstitute()
    self.myLoopSubstitute[loop].setPos(30,30)
    self.myLoopSubstitute[loop].setZValue(3)
    self.myLoopSubstitute[loop].hide()
    self.myScene.scene.addItem(self.myLoopSubstitute[loop])
    
    self.myLoopInsert.append(loop)
    self.myLoopInsert[loop] = LoopInsert()
    self.myLoopInsert[loop].setPos(30,30)
    self.myLoopInsert[loop].setZValue(3)
    self.myLoopInsert[loop].hide()
    self.myScene.scene.addItem(self.myLoopInsert[loop])
    
    self.myLoopMultiply.append(loop)
    self.myLoopMultiply[loop] = LoopMultiply()
    self.myLoopMultiply[loop].setPos(30,30)
    self.myLoopMultiply[loop].setZValue(3)
    self.myLoopMultiply[loop].hide()
    self.myScene.scene.addItem(self.myLoopMultiply[loop])

    self.myWidgetGroup.append(loop)
    self.myWidgetGroup[loop] = self.myScene.scene.createItemGroup([self.myCycleTime[loop], self.myLoopCycles[loop], self.myLoopVelocity[loop], self.myLoopPlay[loop], self.myLoopRecord[loop], self.myLoopOverdub[loop], self.myLoopReplace[loop], self.myLoopSubstitute[loop], self.myLoopInsert[loop], self.myLoopMultiply[loop]])
    self.myWidgetGroup[loop].setPos(loop*100, 0)
    self.myWidgetGroup[loop].setFlag(QGraphicsItem.ItemIsMovable)
    
    self.myScene.view.show()


mySooperLooperWidget = MySooperLooperWidget()

states = ["todo",
          "todo",
          mySooperLooperWidget.myLoopRecord, 
          "todo",
          mySooperLooperWidget.myLoopPlay,
          mySooperLooperWidget.myLoopOverdub,
          mySooperLooperWidget.myLoopMultiply,
          mySooperLooperWidget.myLoopInsert,
          mySooperLooperWidget.myLoopReplace,
          "todo",
          "todo",
          "todo",
          "todo",
          mySooperLooperWidget.myLoopSubstitute,
          "todo"]

#mySooperLooperWidget.currentstate[loopnumber] = mySooperLooperWidget.myLoopPlay

def updateLoopNextState(loopnumber, state):
  state = int(state)
  if states[state] == "todo":
    log("todo this state...")
  else:
    log(states[state])
    currentwidget = mySooperLooperWidget.currentstate[loopnumber]
    getattr(currentwidget[loopnumber], "hide")()
    mySooperLooperWidget.myCycleTime[loopnumber].color = states[state][loopnumber].background
    states[state][loopnumber].nextstate = True
    mySooperLooperWidget.myCycleTime[loopnumber].nextstate = True
    states[state][loopnumber].show()
    if states[state] == mySooperLooperWidget.myLoopRecord:
      mySooperLooperWidget.myCycleTime[loopnumber].background = mySooperLooperWidget.myLoopRecord[loopnumber].background
    else:
      mySooperLooperWidget.myCycleTime[loopnumber].background = mySooperLooperWidget.myCycleTime[loopnumber].defaultbackground
    mySooperLooperWidget.currentstate[loopnumber] = states[state]

def updateLoopState(loopnumber, state):
  state = int(state)
  if states[state] == "todo":
    log("todo this state...")
  else:
    log(states[state])
    currentwidget = mySooperLooperWidget.currentstate[loopnumber]
    getattr(currentwidget[loopnumber], "hide")()
    mySooperLooperWidget.myCycleTime[loopnumber].color = states[state][loopnumber].background
    states[state][loopnumber].nextstate = False
    mySooperLooperWidget.myCycleTime[loopnumber].nextstate = False
    states[state][loopnumber].show()
    if states[state] == mySooperLooperWidget.myLoopRecord:
      mySooperLooperWidget.myCycleTime[loopnumber].background = mySooperLooperWidget.myLoopRecord[loopnumber].background
    else:
      mySooperLooperWidget.myCycleTime[loopnumber].background = mySooperLooperWidget.myCycleTime[loopnumber].defaultbackground
    mySooperLooperWidget.currentstate[loopnumber] = states[state]

def updateVelocity(loopnumber, velocity):
  if velocity <= 0:
    mySooperLooperWidget.myLoopVelocity[loopnumber].velocity = 0
  else:
    mySooperLooperWidget.myLoopVelocity[loopnumber].velocity = (((6.0 * math.log(velocity)/math.log(2.)+198)/198.)**8) * 32
  mySooperLooperWidget.myLoopVelocity[loopnumber].update()

def updateCycleLen(loopnumber, cyclelen):
  mySooperLooperWidget.myCycleTime[loopnumber].cyclelen = cyclelen

def updateLoopLen(loopnumber, looplen):
  if mySooperLooperWidget.myCycleTime[loopnumber].cyclelen != 0:
    mySooperLooperWidget.myLoopCycles[loopnumber].looplen = int(round(looplen/mySooperLooperWidget.myCycleTime[loopnumber].cyclelen)) 
    
def updateLoopPos(loopnumber, looppos):
  if looppos/mySooperLooperWidget.myCycleTime[loopnumber].cyclelen != 0:
    mySooperLooperWidget.myCycleTime[loopnumber].cyclepos = (looppos - (int(looppos/mySooperLooperWidget.myCycleTime[loopnumber].cyclelen) * mySooperLooperWidget.myCycleTime[loopnumber].cyclelen))/mySooperLooperWidget.myCycleTime[loopnumber].cyclelen*360
    mySooperLooperWidget.myLoopCycles[loopnumber].currentloop = int(looppos/mySooperLooperWidget.myCycleTime[loopnumber].cyclelen)
    mySooperLooperWidget.myCycleTime[loopnumber].update()
    mySooperLooperWidget.myLoopCycles[loopnumber].update()

def updateMakeLoop(loop):
  pass
  #oscserver.initOsc(loop)

#QObject.connect(oscserver.emitter, SIGNAL('loopvelocity'), updateVelocity)
oscserver.start()
#oscserver.initOsc()

mySooperLooperWidget.makeLoop(0)
mySooperLooperWidget.makeLoop(1)
mySooperLooperWidget.makeLoop(2)
#mySooperLooperWidget.makeLoop(3)
#mySooperLooperWidget.makeLoop(4)
#mySooperLooperWidget.makeLoop(5)
#mySooperLooperWidget.makeLoop(6)
#mySooperLooperWidget.makeLoop(7)


QObject.connect(oscserver.emitter, SIGNAL('loopvelocity'), updateVelocity)
QObject.connect(oscserver.emitter, SIGNAL('cyclelen'), updateCycleLen)
QObject.connect(oscserver.emitter, SIGNAL('looplen'), updateLoopLen)
QObject.connect(oscserver.emitter, SIGNAL('looppos'), updateLoopPos)
QObject.connect(oscserver.emitter, SIGNAL('loopstate'), updateLoopState)
QObject.connect(oscserver.emitter, SIGNAL('loopnextstate'), updateLoopNextState)

#oscserver.initOsc(0)
#oscserver.initOsc(1)
#oscserver.initOsc(2)
#oscserver.initOsc(3)
#oscserver.initOsc(4)
#oscserver.initOsc(5)
#oscserver.initOsc(6)
#oscserver.initOsc(7)

#app.exec_()

"""
QObject.connect(mySooperLooperWidget, SIGNAL('makeloop'), updateMakeLoop)

mySooperLooperWidget.makeLoop(0)
mySooperLooperWidget.makeLoop(1)
mySooperLooperWidget.makeLoop(2)
mySooperLooperWidget.makeLoop(3)
mySooperLooperWidget.makeLoop(4)


QObject.connect(oscserver.emitter, SIGNAL('loopvelocity'), updateVelocity)
QObject.connect(oscserver.emitter, SIGNAL('cyclelen'), updateCycleLen)
QObject.connect(oscserver.emitter, SIGNAL('looplen'), updateLoopLen)
QObject.connect(oscserver.emitter, SIGNAL('looppos'), updateLoopPos)
QObject.connect(oscserver.emitter, SIGNAL('loopstate'), updateLoopState)

oscserver.initOsc(0)
oscserver.initOsc(1)
oscserver.initOsc(2)
oscserver.initOsc(3)
oscserver.initOsc(4)

states = ["todo", "todo", myLoopRecord, "todo", myLoopPlay, myLoopOverdub, myLoopMultiply, myLoopInsert, myLoopReplace, "todo", "todo", "todo", "todo", myLoopSubstitute, "todo"] 

myScene.view.current = myLoopPlay

def updateVelocity(loopnumber, velocity):
  if velocity <= 0:
    mySooperLooperWidget.myLoopVelocity[loopnumber].velocity = 0
  else:
    mySooperLooperWidget.myLoopVelocity[loopnumber].velocity = (((6.0 * math.log(velocity)/math.log(2.)+198)/198.)**8) * 32
  mySooperLooperWidget.myLoopVelocity[loopnumber].update()
  app.processEvents()

def updateCycleLen(cyclelen):
  myCycleTime.cyclelen = cyclelen

def updateLoopLen(looplen):
  myLoopCycles[loop].looplen = int(round(looplen/myCycleTime.cyclelen)) 
    
def updateLoopPos(looppos):
  myCycleTime.cyclepos = (looppos - (int(looppos/myCycleTime.cyclelen) * myCycleTime.cyclelen))/myCycleTime.cyclelen*360
  myLoopCycles.currentloop = int(looppos/myCycleTime.cyclelen)
  myCycleTime.update()
  myLoopCycles.update()
  app.processEvents()

def updateLoopState(state):
  state = int(state)
  if states[state] == "todo":
    log("todo this state...")
  else:
    log(states[state])
    myScene.view.current.hide()
    myCycleTime.color = states[state].background
    states[state].show()
    if states[state] == myLoopRecord:
      myCycleTime.cyclepos = 360
    myScene.view.current = states[state]


QObject.connect(oscserver.emitter, SIGNAL('loopvelocity'), updateVelocity)
QObject.connect(oscserver.emitter, SIGNAL('cyclelen'), updateCycleLen)
QObject.connect(oscserver.emitter, SIGNAL('looplen'), updateLoopLen)
QObject.connect(oscserver.emitter, SIGNAL('looppos'), updateLoopPos)
QObject.connect(oscserver.emitter, SIGNAL('loopstate'), updateLoopState)

oscserver.start()
oscserver.initOsc()
app.exec_()
"""
