import math

#from sooperlooper_qt import *
#from osc_server import *
from myLogger import *

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
    self.myLoopNumber = []
    self.myWidgetGroup = []
    self.myWidgetEmptyGroup = []
    self.myLoopEmpty = []
    self.myEmptyLoopNumber = []
    self.myEmptyLoopName = []
    self.loops = []
    self.currentstate = []
    self.selected = -1

  def makeLoop(self, loop):
    self.loops.append(loop)
    self.emit(SIGNAL('makeloop'), loop)

    self.currentstate.append(loop)
    self.currentstate[loop] = mySooperLooperWidget.myLoopPlay

    self.myLoopEmpty.append(loop)
    self.myLoopEmpty[loop] = LoopEmpty()
    self.myLoopEmpty[loop].setZValue(0)
    self.myScene.scene.addItem(self.myLoopEmpty[loop])

    self.myCycleTime.append(loop)
    self.myCycleTime[loop] = CycleTime()
    self.myCycleTime[loop].setZValue(5)
    self.myScene.scene.addItem(self.myCycleTime[loop])
    
    self.myLoopCycles.append(loop)
    self.myLoopCycles[loop] = LoopCycles()
    self.myLoopCycles[loop].setPos(15, 15)
    self.myLoopCycles[loop].setZValue(10)
    self.myScene.scene.addItem(self.myLoopCycles[loop])
    
    self.myLoopVelocity.append(loop)
    self.myLoopVelocity[loop] = LoopVelocity()
    self.myLoopVelocity[loop].setPos(24, 24)
    self.myLoopVelocity[loop].setZValue(20)
    self.myScene.scene.addItem(self.myLoopVelocity[loop])

    self.myLoopPlay.append(loop)
    self.myLoopPlay[loop] = LoopPlay()
    self.myLoopPlay[loop].setPos(30, 30)
    self.myLoopPlay[loop].setZValue(30)
    self.myScene.scene.addItem(self.myLoopPlay[loop])

    self.myLoopRecord.append(loop)
    self.myLoopRecord[loop] = LoopRecord()
    self.myLoopRecord[loop].setPos(30, 30)
    self.myLoopRecord[loop].setZValue(30)
    self.myLoopRecord[loop].hide()
    self.myScene.scene.addItem(self.myLoopRecord[loop])
    
    self.myLoopOverdub.append(loop)
    self.myLoopOverdub[loop] = LoopOverdub()
    self.myLoopOverdub[loop].setPos(30,30)
    self.myLoopOverdub[loop].setZValue(30)
    self.myLoopOverdub[loop].hide()
    self.myScene.scene.addItem(self.myLoopOverdub[loop])
    
    self.myLoopReplace.append(loop)
    self.myLoopReplace[loop] = LoopReplace()
    self.myLoopReplace[loop].setPos(30,30)
    self.myLoopReplace[loop].setZValue(30)
    self.myLoopReplace[loop].hide()
    self.myScene.scene.addItem(self.myLoopReplace[loop])
    
    self.myLoopSubstitute.append(loop)
    self.myLoopSubstitute[loop] = LoopSubstitute()
    self.myLoopSubstitute[loop].setPos(30,30)
    self.myLoopSubstitute[loop].setZValue(30)
    self.myLoopSubstitute[loop].hide()
    self.myScene.scene.addItem(self.myLoopSubstitute[loop])
    
    self.myLoopInsert.append(loop)
    self.myLoopInsert[loop] = LoopInsert()
    self.myLoopInsert[loop].setPos(30,30)
    self.myLoopInsert[loop].setZValue(30)
    self.myLoopInsert[loop].hide()
    self.myScene.scene.addItem(self.myLoopInsert[loop])
    
    self.myLoopMultiply.append(loop)
    self.myLoopMultiply[loop] = LoopMultiply()
    self.myLoopMultiply[loop].setPos(30,30)
    self.myLoopMultiply[loop].setZValue(30)
    self.myLoopMultiply[loop].hide()
    self.myScene.scene.addItem(self.myLoopMultiply[loop])

    self.myLoopNumber.append(loop)
    self.myLoopNumber[loop] = LoopNumber()
    self.myLoopNumber[loop].name = str(loop+1)
    getattr(self.myLoopNumber[loop], "setBrush")(Qt.black)
    getattr(self.myLoopNumber[loop], "setText")(self.myLoopNumber[loop].name)
    getattr(self.myLoopNumber[loop], "setPos")(6,6)
    getattr(self.myLoopNumber[loop], "setZValue")(30)
    self.myScene.scene.addItem(self.myLoopNumber[loop])

    self.myEmptyLoopNumber.append(loop)
    self.myEmptyLoopNumber[loop] = LoopNumber()
    self.myEmptyLoopNumber[loop].name = str(loop+1)
    getattr(self.myEmptyLoopNumber[loop], "setBrush")(Qt.black)
    getattr(self.myEmptyLoopNumber[loop], "setText")(self.myEmptyLoopNumber[loop].name)
    getattr(self.myEmptyLoopNumber[loop], "setPos")(6,6)
    getattr(self.myEmptyLoopNumber[loop], "setZValue")(2)
    self.myScene.scene.addItem(self.myEmptyLoopNumber[loop])
    
    self.myEmptyLoopName.append(loop)
    self.myEmptyLoopName[loop] = LoopName()
    self.myEmptyLoopName[loop].name = "loop_" + str(loop+1)
    getattr(self.myEmptyLoopName[loop], "setBrush")(Qt.black)
    getattr(self.myEmptyLoopName[loop], "setText")(self.myEmptyLoopName[loop].name)
    getattr(self.myEmptyLoopName[loop], "setPos")(20,60)
    getattr(self.myEmptyLoopName[loop], "setZValue")(2)
    self.myScene.scene.addItem(self.myEmptyLoopName[loop])

    self.myWidgetEmptyGroup.append(loop)
    self.myWidgetEmptyGroup[loop] = self.myScene.scene.createItemGroup([self.myLoopEmpty[loop], self.myEmptyLoopNumber[loop], self.myEmptyLoopName[loop]])
    self.myWidgetEmptyGroup[loop].setPos(loop*100, 0)
    self.myWidgetEmptyGroup[loop].setZValue(0)
    self.myWidgetEmptyGroup[loop].setFlag(QGraphicsItem.ItemIsMovable)

    self.myWidgetGroup.append(loop)
    self.myWidgetGroup[loop] = self.myScene.scene.createItemGroup([self.myCycleTime[loop], self.myLoopCycles[loop], self.myLoopVelocity[loop], self.myLoopPlay[loop], self.myLoopRecord[loop], self.myLoopOverdub[loop], self.myLoopReplace[loop], self.myLoopSubstitute[loop], self.myLoopInsert[loop], self.myLoopMultiply[loop], self.myLoopNumber[loop]])
    self.myWidgetGroup[loop].setPos(loop*100, 0)
    self.myWidgetGroup[loop].setZValue(10)
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
  if mySooperLooperWidget.myCycleTime[loopnumber].cyclelen != 0:
    mySooperLooperWidget.myCycleTime[loopnumber].cyclepos = (looppos - (int(looppos/mySooperLooperWidget.myCycleTime[loopnumber].cyclelen) * mySooperLooperWidget.myCycleTime[loopnumber].cyclelen))/mySooperLooperWidget.myCycleTime[loopnumber].cyclelen*360
    mySooperLooperWidget.myLoopCycles[loopnumber].currentloop = int(looppos/mySooperLooperWidget.myCycleTime[loopnumber].cyclelen)
    mySooperLooperWidget.myCycleTime[loopnumber].update()
    mySooperLooperWidget.myLoopCycles[loopnumber].update()

def updateMakeLoop(loop):
  pass
  #oscserver.initOsc(loop)

def updateSelectedLoopNum(loopnum):
  if mySooperLooperWidget.selected != -1:
    mySooperLooperWidget.myWidgetGroup[mySooperLooperWidget.selected].scale(.3125, .3125)
  
    if mySooperLooperWidget.selected <= 3:
      mySooperLooperWidget.myWidgetGroup[mySooperLooperWidget.selected].setPos(0, mySooperLooperWidget.selected*100)
    else:
      mySooperLooperWidget.myWidgetGroup[mySooperLooperWidget.selected].setPos((mySooperLooperWidget.selected-3)*100,300)

  log("%s / %s" % (str(mySooperLooperWidget.selected), str(int(loopnum))))
  mySooperLooperWidget.selected = int(loopnum)
  if loopnum != -1:
    mySooperLooperWidget.myWidgetGroup[mySooperLooperWidget.selected].scale(3.2, 3.2)
    mySooperLooperWidget.myWidgetGroup[mySooperLooperWidget.selected].setPos(88, -8)
  

def updateLoopName(loopnum, name):
  mySooperLooperWidget.myEmptyLoopName[loopnum].name = name
  textRect = QRectF()
  mySooperLooperWidget.myEmptyLoopName[loopnum].sizeName = len(mySooperLooperWidget.myEmptyLoopName[loopnum].name)

  def resizeName():
    mySooperLooperWidget.myEmptyLoopName[loopnum].setText(mySooperLooperWidget.myEmptyLoopName[loopnum].name[:mySooperLooperWidget.myEmptyLoopName[loopnum].sizeName])
    textRect = mySooperLooperWidget.myEmptyLoopName[loopnum].boundingRect()
    textRectList = textRect.getCoords()
    if int(textRectList[2]) > 71:
      mySooperLooperWidget.myEmptyLoopName[loopnum].sizeName -= 1
      resizeName()
    else:
      return None

  resizeName()

slwets = [['cc', '12', 0], ['cc', '13', 1], ['cc', '14', 2], ['cc', '15', 3], ['cc', '16', 4], ['cc', '17', 5], ['cc', '18', 6], ['axis', '3', -3, '0-1']]

slloopnums = [['cc', '30', 0], ['cc', '31', 1], ['cc', '69', 2], ['pc', '4', 3], ['pc', '5', 4], ['pc', '6', 5], ['pc', '7', 6], ['button', '4', 0], ['button', '1', 1], ['button', '3', 2], ['button', '2', 3]] 

slstates = [['cc', '1', 'record'], ['cc', '67', 'overdub'], ['cc', '68', 'substitute'], ['cc', '66', 'multiply']]

def slDispatch(type, param, value):
  for slwet in slwets:
    if slwet[0] == type and slwet[1] == param:
      if len(slwet) >= 3:
        # if slwet[3] == 'cont': gamepad.bridge.emitMessage(
        oscserver.sendLoopVelocity(slwet[2], float(value))
      else:
        value = 1 - (int(value)/127.)
        valuef = 2.** ((math.sqrt(math.sqrt(math.sqrt(value)))*198.-198)/6.)
        oscserver.sendLoopVelocity(slwet[2], float(valuef))
  for slloopnum in slloopnums:
    if slloopnum[0] == type and slloopnum[1] == param:
      oscserver.sendSelectedLoopNum(slloopnum[2])
  for slstate in slstates:
    if slstate[0] == type and slstate[1] == param:
      oscserver.sendHit(-3, slstate[2])

oscserver.start()
#oscserver.initOsc()

mySooperLooperWidget.makeLoop(0)
mySooperLooperWidget.makeLoop(1)
mySooperLooperWidget.makeLoop(2)
mySooperLooperWidget.makeLoop(3)
mySooperLooperWidget.makeLoop(4)
mySooperLooperWidget.makeLoop(5)
mySooperLooperWidget.makeLoop(6)


QObject.connect(oscserver.emitter, SIGNAL('loopvelocity'), updateVelocity)
QObject.connect(oscserver.emitter, SIGNAL('cyclelen'), updateCycleLen)
QObject.connect(oscserver.emitter, SIGNAL('looplen'), updateLoopLen)
QObject.connect(oscserver.emitter, SIGNAL('looppos'), updateLoopPos)
QObject.connect(oscserver.emitter, SIGNAL('loopstate'), updateLoopState)
QObject.connect(oscserver.emitter, SIGNAL('loopnextstate'), updateLoopNextState)
QObject.connect(oscserver.emitter, SIGNAL('selectedloopnum'), updateSelectedLoopNum)
QObject.connect(midi.bridge, SIGNAL('MIDI'), slDispatch)
QObject.connect(gamepad.bridge, SIGNAL('gamepad'), slDispatch)

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
## 4x4 grid layout with one big at top right which goes from (1,0) to (2,3)
_ip.magic("run -i sooperlooper_qt.py")
_ip.magic("run -i osc_server.py")
_ip.magic("run -i midi_dispatcher.py")
_ip.magic("run -i gamepad_dispatcher.py")
_ip.magic("run -i ipython_test2.py")

midi.start()
gamepad.start()

oscserver.initOsc(0)
oscserver.initOsc(1)
oscserver.initOsc(2)
oscserver.initOsc(3)
oscserver.initOsc(4)
oscserver.initOsc(5)
oscserver.initOsc(6)
mySooperLooperWidget.myWidgetGroup[1].setPos(0,100)
mySooperLooperWidget.myWidgetEmptyGroup[1].setPos(0,100)
mySooperLooperWidget.myWidgetGroup[2].setPos(0,200)
mySooperLooperWidget.myWidgetEmptyGroup[2].setPos(0,200)
mySooperLooperWidget.myWidgetGroup[3].setPos(0,300)
mySooperLooperWidget.myWidgetEmptyGroup[3].setPos(0,300)
mySooperLooperWidget.myWidgetGroup[4].setPos(100,300)
mySooperLooperWidget.myWidgetEmptyGroup[4].setPos(100,300)
mySooperLooperWidget.myWidgetGroup[5].setPos(200,300)
mySooperLooperWidget.myWidgetEmptyGroup[5].setPos(200,300)
mySooperLooperWidget.myWidgetGroup[6].setPos(300,300)
mySooperLooperWidget.myWidgetEmptyGroup[6].setPos(300,300)

#mySooperLooperWidget.myWidgetGroup[0].scale(3.2,3.2)
#mySooperLooperWidget.myWidgetGroup[0].setPos(88,-8)

mySooperLooperWidget.myScene.scene.setBackgroundBrush(Qt.gray)
mySooperLooperWidget.myScene.view.setWindowTitle("topot_sooperlooper")
mySooperLooperWidget.myScene.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
mySooperLooperWidget.myScene.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

mySooperLooperWidget.myScene.view.setGeometry(0,0,600,600)

allTogether = mySooperLooperWidget.myScene.scene.createItemGroup([mySooperLooperWidget.myWidgetGroup[0], mySooperLooperWidget.myWidgetGroup[1], mySooperLooperWidget.myWidgetGroup[2], mySooperLooperWidget.myWidgetGroup[3], mySooperLooperWidget.myWidgetGroup[4], mySooperLooperWidget.myWidgetGroup[5], mySooperLooperWidget.myWidgetGroup[6], mySooperLooperWidget.myWidgetEmptyGroup[0], mySooperLooperWidget.myWidgetEmptyGroup[1], mySooperLooperWidget.myWidgetEmptyGroup[2], mySooperLooperWidget.myWidgetEmptyGroup[3], mySooperLooperWidget.myWidgetEmptyGroup[4], mySooperLooperWidget.myWidgetEmptyGroup[5], mySooperLooperWidget.myWidgetEmptyGroup[6]])

allTogether.scale(1.5, 1.5)

brush = QBrush()
brush.setColor(Qt.darkCyan)
brush.setStyle(Qt.Dense4Pattern)
mySooperLooperWidget.myScene.scene.setBackgroundBrush(brush)
allTogether.setPos(70,150)

mySooperLooperWidget.myWidgetGroup[0].scale(.3125, .3125)
mySooperLooperWidget.myWidgetGroup[0].setPos(0,100)
"""
