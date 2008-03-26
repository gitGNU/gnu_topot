from myLogger import *
import math

myCycleTime = CycleTime()
myCycleTime.setZValue(0)
myScene.scene.addItem(myCycleTime)

myLoopCycles = LoopCycles()
myLoopCycles.setPos(15, 15)
myLoopCycles.setZValue(1)
myScene.scene.addItem(myLoopCycles)

myLoopVelocity = LoopVelocity()
myLoopVelocity.setPos(24, 24)
myLoopVelocity.setZValue(2)
myScene.scene.addItem(myLoopVelocity)

myLoopPlay = LoopPlay()
myLoopPlay.setPos(30, 30)
myLoopPlay.setZValue(3)
myScene.scene.addItem(myLoopPlay)

myLoopRecord = LoopRecord()
myLoopRecord.setPos(30, 30)
myLoopRecord.setZValue(3)
myLoopRecord.hide()
myScene.scene.addItem(myLoopRecord)

myLoopOverdub = LoopOverdub()
myLoopOverdub.setPos(30,30)
myLoopOverdub.setZValue(3)
myLoopOverdub.hide()
myScene.scene.addItem(myLoopOverdub)

myLoopReplace = LoopReplace()
myLoopReplace.setPos(30,30)
myLoopReplace.setZValue(3)
myLoopReplace.hide()
myScene.scene.addItem(myLoopReplace)

myLoopSubstitute = LoopSubstitute()
myLoopSubstitute.setPos(30,30)
myLoopSubstitute.setZValue(3)
myLoopSubstitute.hide()
myScene.scene.addItem(myLoopSubstitute)

myLoopInsert = LoopInsert()
myLoopInsert.setPos(30,30)
myLoopInsert.setZValue(8)
myLoopInsert.hide()
myScene.scene.addItem(myLoopInsert)

myLoopMultiply = LoopMultiply()
myLoopMultiply.setPos(30,30)
myLoopMultiply.setZValue(3)
myLoopMultiply.hide()
myScene.scene.addItem(myLoopMultiply)

itemsGroup = myScene.scene.createItemGroup([myCycleTime, myLoopCycles, myLoopVelocity, myLoopPlay, myLoopRecord, myLoopOverdub, myLoopReplace, myLoopSubstitute, myLoopInsert, myLoopMultiply])
itemsGroup.setFlag(QGraphicsItem.ItemIsMovable)

myScene.view.show()

states = ["todo", "todo", myLoopRecord, "todo", myLoopPlay, myLoopOverdub, myLoopMultiply, myLoopInsert, myLoopReplace, "todo", "todo", "todo", "todo", myLoopSubstitute, "todo"] 

myScene.view.current = myLoopPlay

def updateVelocity(velocity):
  if velocity <= 0:
    myLoopVelocity.velocity = 0
  else:
    myLoopVelocity.velocity = (((6.0 * math.log(velocity)/math.log(2.)+198)/198.)**8) * 32
  myLoopVelocity.update()
  app.processEvents()

def updateCycleLen(cyclelen):
  myCycleTime.cyclelen = cyclelen

def updateLoopLen(looplen):
  myLoopCycles.looplen = int(round(looplen/myCycleTime.cyclelen)) 
    
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

