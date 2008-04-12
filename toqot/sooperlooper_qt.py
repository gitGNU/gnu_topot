from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class MainForm(QDialog):
  def __init__(self, parent=None):
    super(MainForm, self).__init__(parent)

    self.scene = QGraphicsScene(self)
    self.scene.setSceneRect(0, 0, 200, 200)
    self.view = QGraphicsView()
    self.view.setRenderHint(QPainter.Antialiasing)
    self.view.setScene(self.scene)
    self.view.setFocusPolicy(Qt.NoFocus)

  def zoom(self, value):
    factor = value/100.0
    matrix = self.view.matrix()
    matrix.reset()
    matrix.scale(factor, factor)
    self.view.setMatrix(matrix)

class CycleTime(QGraphicsItem):
  Rect = QRectF(0, 0, 100,100)
  def __init__(self, parent = None):
    super(CycleTime, self).__init__(parent)
    self.rectangle = QRectF(5.0, 5.0, 90.0, 90.0)
    self.defaultbackground = Qt.lightGray
    self.background = Qt.lightGray
    self.color = QColor(255, 0, 32)
    self.cyclepos = 0
    self.cyclelen = 1
    self.pen = QPen()
    self.pen.setWidth(1)

  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    painter.setBrush(self.background)
    painter.setPen(self.pen)
    painter.drawEllipse(self.rectangle)

    painter.setBrush(self.color)
    painter.drawPie(self.rectangle, 90*16, -self.cyclepos *16)

class LoopCycles(QGraphicsItem):
  Rect = QRectF(0, 0, 70,70)
  def __init__(self, parent = None):
    super(LoopCycles, self).__init__(parent)
    self.rectangle = QRectF(0.0, 0.0, 70.0, 70.0)
    self.color = Qt.darkCyan
    self.looplen = 1
    self.currentloop = 0
    self.pen = QPen()
    self.pen.setWidth(1)

  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    painter.setBrush(Qt.lightGray)
    painter.setPen(self.pen)
    painter.drawEllipse(self.rectangle)

    for i in range(self.looplen):
      if i <= self.currentloop:
        painter.setBrush(self.color)
      else:
        painter.setBrush(Qt.lightGray)
      painter.drawPie(self.rectangle, (90-((360./self.looplen)*i))*16, (360./self.looplen) * 16 * -1)
 
class LoopVelocity(QGraphicsItem):
  Rect = QRectF(0.0, 0.0, 52.0, 52.0)
  def __init__(self, parent = None):
    super(LoopVelocity, self).__init__(parent)
    self.rectangle = QRectF(0.0, 0.0, 52.0, 52.0)
    self.color = QColor(255, 140, 0)
    self.color80 = Qt.red
    self.color90 = Qt.darkRed
    self.resolution = 32
    self.velocity = 0
    self.pen = QPen()
    self.pen.setWidth(1)

  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    painter.setBrush(Qt.lightGray)
    painter.setPen(self.pen)
    painter.drawEllipse(self.rectangle)

    for i in range(self.resolution):
      if i <= self.velocity:
        if i >= round(self.resolution * .8):
          painter.setBrush(self.color90)
        elif i >= round(self.resolution * .7) and i < round(self.resolution * .8):
          painter.setBrush(self.color80)
        else:
          painter.setBrush(self.color)
      else:
        painter.setBrush(Qt.lightGray)
      painter.drawPie(self.rectangle, (90-((360./self.resolution)*i))*16, (360./self.resolution) * 16 * -1)

class LoopPlay(QGraphicsItem):
  Rect = QRectF(0.0, 0.0, 40.0, 40.0)
  def __init__(self, parent = None):
    super(LoopPlay, self).__init__(parent)
    self.brush = QBrush()
    self.nextstate = False
    self.rectangle = QRectF(0.0, 0.0, 40.0, 40.0)
    self.triangle = QPolygon()
    self.triangle.setPoints(15, 10, 30, 20, 15, 30)
    self.background = Qt.green
    self.color = Qt.black
    self.pen = QPen()
    self.pen.setWidth(1)
    self.pen.setCapStyle(Qt.RoundCap)
    self.pen.setJoinStyle(Qt.RoundJoin)

  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    
    if not self.nextstate:
      painter.setBrush(self.background)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)  
    else:           
      painter.setBrush(self.color)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)
      
      self.brush.setColor(self.background)
      self.brush.setStyle(Qt.Dense3Pattern) # texture
   
      painter.setBrush(self.brush)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)

    painter.setBrush(self.color)
    painter.drawPolygon(self.triangle)

class LoopRecord(QGraphicsItem):
  Rect = QRectF(0.0, 0.0, 40.0, 40.0)
  def __init__(self, parent = None):
    super(LoopRecord, self).__init__(parent)
    self.brush = QBrush()
    self.nextstate = False
    self.rectangle = QRectF(0.0, 0.0, 40.0, 40.0)
    self.background = QColor(255, 0, 32)
    self.circle = QRectF(15.0, 15.0, 10.0, 10.0)
    self.color = Qt.black
    self.pen = QPen()
    self.pen.setWidth(1)

  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    if not self.nextstate:
      painter.setBrush(self.background)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)  
    else:           
      painter.setBrush(self.color)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)
      
      self.brush.setColor(self.background)
      self.brush.setStyle(Qt.Dense3Pattern) # texture
   
      painter.setBrush(self.brush)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)

    painter.setBrush(self.color)
    painter.drawEllipse(self.circle)

class LoopOverdub(QGraphicsItem):
  Rect = QRectF(0.0, 0.0, 40.0, 40.0)
  def __init__(self, parent = None):
    super(LoopOverdub, self).__init__(parent)
    self.brush = QBrush()
    self.nextstate = False
    self.rectangle = QRectF(0.0, 0.0, 40.0, 40.0)
    self.background = QColor(255, 0, 32)
    self.leftcircle = QRectF(10.0, 15.0, 10.0, 10.0)
    self.rightcircle = QRectF(20.0, 15.0, 10.0, 10.0)
    self.color = Qt.black
    self.pen = QPen()
    self.pen.setWidth(1)
   
  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    if not self.nextstate:
      painter.setBrush(self.background)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)  
    else:           
      painter.setBrush(self.color)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)
      
      self.brush.setColor(self.background)
      self.brush.setStyle(Qt.Dense3Pattern) # texture
   
      painter.setBrush(self.brush)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)

    painter.setBrush(self.color)
    painter.drawEllipse(self.leftcircle)
    painter.drawEllipse(self.rightcircle)

class LoopReplace(QGraphicsItem):
  Rect = QRectF(0.0, 0.0, 40.0, 40.0)
  def __init__(self, parent = None):
    super(LoopReplace, self).__init__(parent)
    self.brush = QBrush()
    self.nextstate = False
    self.rectangle = QRectF(0.0, 0.0, 40.0, 40.0)
    self.circle = QRectF(20.0, 15.0, 10.0, 10.0)
    self.background = QColor(255, 0, 32)
    self.color = Qt.black
    self.pen = QPen()
    self.pen.setWidth(1)
    self.pen2 = QPen()
    self.pen2.setWidth(4)
    self.pen2.setCapStyle(Qt.RoundCap)

  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    if not self.nextstate:
      painter.setBrush(self.background)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)  
    else:           
      painter.setBrush(self.color)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)
      
      self.brush.setColor(self.background)
      self.brush.setStyle(Qt.Dense3Pattern) # texture
   
      painter.setBrush(self.brush)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)

    painter.setBrush(self.color)
    painter.drawEllipse(self.circle)
    painter.setPen(self.pen2)
    painter.drawLine(15,20, 20,20)

class LoopSubstitute(QGraphicsItem):
  Rect = QRectF(0.0, 0.0, 40.0, 40.0)
  def __init__(self, parent = None):
    super(LoopSubstitute, self).__init__(parent)
    self.brush = QBrush()
    self.nextstate = False
    self.rectangle = QRectF(0.0, 0.0, 40.0, 40.0)
    self.circle = QRectF(20.0, 15.0, 10.0, 10.0)
    self.triangle = QPolygon()
    self.triangle.setPoints(12, 14, 22, 20, 12, 26)
    self.background = QColor(255, 0, 32)
    self.color = Qt.black
    self.pen = QPen()
    self.pen.setWidth(1)
    self.pen.setCapStyle(Qt.RoundCap)
    self.pen.setJoinStyle(Qt.RoundJoin)


  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    if not self.nextstate:
      painter.setBrush(self.background)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)  
    else:           
      painter.setBrush(self.color)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)
      
      self.brush.setColor(self.background)
      self.brush.setStyle(Qt.Dense3Pattern) # texture
   
      painter.setBrush(self.brush)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)

    painter.setBrush(self.color)
    painter.drawEllipse(self.circle)
    painter.drawPolygon(self.triangle)

class LoopInsert(QGraphicsItem):
  Rect = QRectF(0.0, 0.0, 40.0, 40.0)
  def __init__(self, parent = None):
    super(LoopInsert, self).__init__(parent)
    self.brush = QBrush()
    self.nextstate = False
    self.rectangle = QRectF(0.0, 0.0, 40.0, 40.0)
    self.leftcircle = QRectF(7.5, 15.0, 10.0, 10.0)
    self.rightcircle = QRectF(22.5, 15.0, 10.0, 10.0)
    self.background = QColor(255, 0, 32)
    self.color = Qt.black
    self.pen = QPen()
    self.pen.setWidth(1)
    self.pen2 = QPen()
    self.pen2.setWidth(4)
    self.pen2.setCapStyle(Qt.RoundCap)

  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    if not self.nextstate:
      painter.setBrush(self.background)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)  
    else:           
      painter.setBrush(self.color)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)
      
      self.brush.setColor(self.background)
      self.brush.setStyle(Qt.Dense3Pattern) # texture
   
      painter.setBrush(self.brush)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)

    painter.setBrush(self.color)
    painter.drawEllipse(self.leftcircle)
    painter.drawEllipse(self.rightcircle)
    painter.setPen(self.pen2)
    painter.drawLine(12.5 ,20, 25, 20)

class LoopMultiply(QGraphicsItem):
  Rect = QRectF(0.0, 0.0, 40.0, 40.0)
  def __init__(self, parent = None):
    super(LoopMultiply, self).__init__(parent)
    self.brush = QBrush()
    self.nextstate = False
    self.rectangle = QRectF(0.0, 0.0, 40.0, 40.0)
    self.background = QColor(255, 0, 32)
    self.leftcircle = QRectF(7.5, 15.0, 10.0, 10.0)
    self.circle = QRectF(15.0, 15.0, 10.0, 10.0)
    self.rightcircle = QRectF(22.5, 15.0, 10.0, 10.0)
    self.color = Qt.black
    self.pen = QPen()
    self.pen.setWidth(1)
   
  def boundingRect(self):
    return self.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(self.Rect)
    return path

  def paint(self, painter, option, widget):
    if not self.nextstate:
      painter.setBrush(self.background)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)  
    else:           
      painter.setBrush(self.color)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)
      
      self.brush.setColor(self.background)
      self.brush.setStyle(Qt.Dense3Pattern) # texture
   
      painter.setBrush(self.brush)
      painter.setPen(self.pen)
      painter.drawEllipse(self.rectangle)

    painter.setBrush(self.color)
    painter.drawEllipse(self.leftcircle)
    painter.drawEllipse(self.circle)
    painter.drawEllipse(self.rightcircle)



app = QApplication(sys.argv)
myScene = MainForm()

"""tests:
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
myLoopRecord.setZValue(4)
myScene.scene.addItem(myLoopRecord)

myLoopOverdub = LoopOverdub()
myLoopOverdub.setPos(30,30)
myLoopOverdub.setZValue(5)
myScene.scene.addItem(myLoopOverdub)

myLoopReplace = LoopReplace()
myLoopReplace.setPos(30,30)
myLoopReplace.setZValue(6)
myScene.scene.addItem(myLoopReplace)

myLoopSubstitute = LoopSubstitute()
myLoopSubstitute.setPos(30,30)
myLoopSubstitute.setZValue(7)
myScene.scene.addItem(myLoopSubstitute)

myLoopInsert = LoopInsert()
myLoopInsert.setPos(30,30)
myLoopInsert.setZValue(8)
myScene.scene.addItem(myLoopInsert)

myLoopMultiply = LoopMultiply()
myLoopMultiply.setPos(30,30)
myLoopMultiply.setZValue(9)
myScene.scene.addItem(myLoopMultiply)

myScene.view.show()

itemsGroup = myScene.scene.createItemGroup([myCycleTime, myLoopCycles, myLoopVelocity, myLoopPlay, myLoopRecord, myLoopOverdub, myLoopReplace, myLoopSubstitute, myLoopInsert, myLoopMultiply])
itemsGroup.setFlag(QGraphicsItem.ItemIsMovable)
itemsGroup.scale(2,2)

myLoopMultiply.hide()
myLoopInsert.hide()
myLoopSubstitute.hide()
myLoopReplace.hide()
myLoopOverdub.hide()
myLoopRecord.hide()
myLoopRecord.show()
myLoopOverdub.show()
myLoopReplace.show()
myLoopSubstitute.show()
myLoopInsert.show()
myLoopMultiply.show()
"""
