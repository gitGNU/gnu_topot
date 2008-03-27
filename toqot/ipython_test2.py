
#from sooperlooper_qt import *

class MySooperLooperWidget:
  def __init__(self):
    self.myScene = MainForm()
    self.myCycleTime = []
    self.myLoopCycles = []
    self.myLoopVelocity = []
    self.myLoopPlay = []
    self.myWidgetGroup = []
    self.loops = []

  def makeLoop(self, loop):
    self.loops.append(loop)
    
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

    self.myLoopRecord[loop] = LoopRecord()
    self.myLoopRecord[loop].setPos(30, 30)
    self.myLoopRecord[loop].setZValue(3)
    self.myLoopRecord[loop].hide()
    self.myScene.scene.addItem(self.myLoopRecord[loop])
    
    self.myLoopOverdub[loop] = LoopOverdub()
    self.myLoopOverdub[loop].setPos(30,30)
    self.myLoopOverdub[loop].setZValue(3)
    self.myLoopOverdub[loop].hide()
    self.myScene.scene.addItem(self.myLoopOverdub[loop])
    
    self.myLoopReplace[loop] = LoopReplace()
    self.myLoopReplace[loop].setPos(30,30)
    self.myLoopReplace[loop].setZValue(3)
    self.myLoopReplace[loop].hide()
    self.myScene.scene.addItem(self.myLoopReplace[loop])
    
    self.myLoopSubstitute[loop] = LoopSubstitute()
    self.myLoopSubstitute[loop].setPos(30,30)
    self.myLoopSubstitute[loop].setZValue(3)
    self.myLoopSubstitute[loop].hide()
    self.myScene.scene.addItem(self.myLoopSubstitute[loop])
    
    self.myLoopInsert[loop] = LoopInsert()
    self.myLoopInsert[loop].setPos(30,30)
    self.myLoopInsert[loop].setZValue(8)
    self.myLoopInsert[loop].hide()
    self.myScene.scene.addItem(self.myLoopInsert[loop])
    
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



"""
self.myLoopRecord[loop] = LoopRecord()
self.myLoopRecord[loop].setPos(30, 30)
self.myLoopRecord[loop].setZValue(3)
self.myLoopRecord[loop].hide()
self.myScene.scene.addItem(self.myLoopRecord[loop])

self.myLoopOverdub[loop] = LoopOverdub()
self.myLoopOverdub[loop].setPos(30,30)
self.myLoopOverdub[loop].setZValue(3)
self.myLoopOverdub[loop].hide()
self.myScene.scene.addItem(self.myLoopOverdub[loop])

self.myLoopReplace[loop] = LoopReplace()
self.myLoopReplace[loop].setPos(30,30)
self.myLoopReplace[loop].setZValue(3)
self.myLoopReplace[loop].hide()
self.myScene.scene.addItem(self.myLoopReplace[loop])

self.myLoopSubstitute[loop] = LoopSubstitute()
self.myLoopSubstitute[loop].setPos(30,30)
self.myLoopSubstitute[loop].setZValue(3)
self.myLoopSubstitute[loop].hide()
self.myScene.scene.addItem(self.myLoopSubstitute[loop])

self.myLoopInsert[loop] = LoopInsert()
self.myLoopInsert[loop].setPos(30,30)
self.myLoopInsert[loop].setZValue(8)
self.myLoopInsert[loop].hide()
self.myScene.scene.addItem(self.myLoopInsert[loop])

self.myLoopMultiply[loop] = LoopMultiply()
self.myLoopMultiply[loop].setPos(30,30)
self.myLoopMultiply[loop].setZValue(3)
self.myLoopMultiply[loop].hide()
self.myScene.scene.addItem(self.myLoopMultiply[loop])

itemsGroup = self.myScene.scene.createItemGroup([self.myCycleTime, self.myLoopCycles, self.myLoopVelocity, self.myLoopPlay, self.myLoopRecord[loop], self.myLoopOverdub[loop], self.myLoopReplace[loop], self.myLoopSubstitute[loop], self.myLoopInsert[loop], self.myLoopMultiply[loop]])
itemsGroup.setFlag(QGraphicsItem.ItemIsMovable)

self.myScene.view.show()

states = ["todo", "todo", self.myLoopRecord[loop], "todo", self.myLoopPlay, self.myLoopOverdub[loop], self.myLoopMultiply[loop], self.myLoopInsert[loop], self.myLoopReplace[loop], "todo", "todo", "todo", "todo", self.myLoopSubstitute[loop], "todo"] 

self.myScene.view.current = self.myLoopPlay
"""
