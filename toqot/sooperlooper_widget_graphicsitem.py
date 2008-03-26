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




class MyLittleDisplay(QGraphicsItem):
  Rect = QRectF(0,0, 100,100)
  def __init__(self, parent = None):
    super(MyLittleDisplay, self).__init__(parent)
    self.looplen = 5
    self.velocity = 0
    #self.painter = QPainter()
    self.rectangle = QRectF(5.0, 5.0, 90.0, 90.0)
    self.rectangle2 = QRectF(15.0, 15.0, 70.0, 70.0)
    self.rectangle3 = QRectF(24.0, 24.0, 52.0, 52.0)
    self.rectangle4 = QRectF(30.0, 30.0, 40.0, 40.0)
    self.rectangle5 = QRectF(45.0, 45.0, 10.0, 10.0)
    self.rectangle6 = QRectF(40.0, 45.0, 10.0, 10.0)
    self.rectangle7 = QRectF(50.0, 45.0, 10.0, 10.0)
    self.rectangle8 = QRectF(55.0, 45.0, 10.0, 10.0)
    self.rectangle9 = QRectF(35.0, 45.0, 10.0, 10.0)
    self.triangle = QPolygon()
    self.triangle.setPoints(45, 40, 60, 50, 45, 60)
    self.triangle2 = QPolygon()
    self.triangle2.setPoints(42, 42, 52, 50, 42, 58)
    self.pen = QPen()
    self.pen.setWidth(1)
    self.pen.setColor(Qt.red)
    self.pen2 = QPen()
    self.pen2.setWidth(3)
    self.pen2.setColor(Qt.black)
    self.pen3 = QPen()
    self.pen3.setWidth(1)
    self.pen3.setColor(Qt.black)

  def boundingRect(self):
    return MyLittleDisplay.Rect

  def shape(self):
    path = QPainterPath()
    path.addEllipse(MyLittleDisplay.Rect)
    return path

  def paint(self, painter, option, widget):
    self.painter = painter
    #self.painter.begin(self)
    #self.painter.setRenderHint(QPainter.Antialiasing)

    ## loop's time ring
    self.painter.setBrush(Qt.lightGray)
    self.painter.setPen(self.pen3)
    self.painter.drawEllipse(self.rectangle)

    #self.painter.setBrush(QColor(0, 192, 64))  #when play
    self.painter.setBrush(QColor(255, 0, 32))   #when record
    self.painter.setPen(self.pen3)
    self.painter.drawPie(self.rectangle, 90*16, -self.velocity*16)
    
    ## the length of loop
    self.painter.setBrush(Qt.lightGray)
    self.painter.setPen(self.pen3)
    self.painter.drawEllipse(self.rectangle2)
   
    for i in range(self.looplen):
      if i < 1:
        self.painter.setBrush(Qt.darkCyan)
      else:
        self.painter.setBrush(Qt.lightGray)
      
      self.painter.setPen(self.pen3)
      self.painter.drawPie(self.rectangle2, (90-((360./self.looplen)*i))*16, (360./self.looplen) * 16 * -1)
   
    ## velocity
    for i in range(32):
      if i < 24:
        self.painter.setBrush(QColor(255,255,0))
      else:
        self.painter.setBrush(Qt.lightGray)
      self.painter.setPen(self.pen3)
      self.painter.drawPie(self.rectangle3, (90-((360./32)*i))*16, (360./32) * 16 * -1)
   
    ## play (green)
    #self.painter.setBrush(Qt.darkGreen)
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle4)

    #self.painter.setBrush(Qt.black)
    #self.painter.setPen(self.pen3)
    #self.painter.drawPolygon(self.triangle)

    ## record (red)
    self.painter.setBrush(QColor(255, 0, 32))
    self.painter.setPen(self.pen3)
    self.painter.drawEllipse(self.rectangle4)

    self.painter.setBrush(Qt.black)
    self.painter.setPen(self.pen3)
    self.painter.drawEllipse(self.rectangle5)

    ## overdub (red)
    #self.painter.setBrush(QColor(255, 0, 32))
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle4)

    #self.painter.setBrush(Qt.black)
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle6)
    #self.painter.drawEllipse(self.rectangle7)

    ## replace (red)
    #self.painter.setBrush(QColor(255, 0, 32))
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle4)

    #self.painter.setBrush(Qt.black)
    #self.painter.setPen(self.pen2)
    #self.painter.drawLine(45,50, 50,50)
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle7)

    ## substitute (red)
    #self.painter.setBrush(QColor(255, 0, 32))
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle4)

    #self.painter.setBrush(Qt.black)
    #self.painter.drawEllipse(self.rectangle7)
    #self.painter.drawPolygon(self.triangle2)

    ## insert (red)
    #self.painter.setBrush(QColor(255, 0, 32))
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle4)

    #self.painter.setBrush(Qt.black)
    #self.painter.setPen(self.pen2)
    #self.painter.drawLine(45,50, 55,50)
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle8)
    #self.painter.drawEllipse(self.rectangle9)
    
    ## multiply (red)
    #self.painter.setBrush(QColor(255, 0, 32))
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle4)

    #self.painter.setBrush(Qt.black)
    #self.painter.setPen(self.pen3)
    #self.painter.drawEllipse(self.rectangle5)
    #self.painter.drawEllipse(self.rectangle8)
    #self.painter.drawEllipse(self.rectangle9)
    
    # mute on any
    #self.painter.setBrush(QColor(192,192,192,192))
    #self.painter.drawEllipse(self.rectangle4)


    #self.painter.end()


app = QApplication(sys.argv)
myScene = MainForm()
myGraphicsItem = MyLittleDisplay()
myScene.scene.addItem(myGraphicsItem)
myScene.view.show()

""" tests:
myScene.view.setWindowTitle("topot")
myGraphicsItem.moveBy(10,10)
myGraphicsItem.scale(2,2)
myGraphicsItem.rotate(90)
myGraphicsItem.setFlag(QGraphicsItem.ItemIsMovable)
myGraphicsItem.setZValue(2)
myGraphicsItem.setZValue(0)
myGraphicsItem2.setPos(100,100)
myGraphicsItem.setToolTip("channel_1")
myScene.zoom(140)
def rokaj(stop, start = 0, step = 1):
  for i in range(start, stop, step):
    myGraphicsItem.velocity = i
    myGraphicsItem.update()
    app.processEvents()

time rokaj(360)
### TODO ItemGroup
"""
