from PyQt4.QtCore import *
from PyQt4.QtGui import *
import liblo
import sys

from sooperlooper_qt import *

from myLogger import *

SOOPERLOOPER_SERVER_PORT = 9951
SERVER_PORT = "1234"

class Emitter(QObject):
  def __init__(self, parent = None):
        super(Emitter, self).__init__(parent)

  def emitM(self, signal, message):
    self.emit(SIGNAL(signal), message)

class OscSooperLooper(QThread):
  def __init__(self, parent=None):
    QThread.__init__(self, parent)
    self.emitter = Emitter() 
    self.loop = "0"
    self.target = liblo.Address(SOOPERLOOPER_SERVER_PORT)

    try:
      self.server = liblo.Server(1234)
    except liblo.ServerError, err:
      log(str(err))
      sys.exit()
 
  def run(self):
    self.startOscServer()
    self.exec_()

  def initOsc(self):
    liblo.send(self.target, '/ping', 'osc.udp://localhost:%s' % SERVER_PORT, '/loopcount')
    liblo.send(self.target, '/sl/%d/get' % self.loop, 'state', 'osc.udp://localhost:%s' % SERVER_PORT, '/loopstate')
    liblo.send(self.target, '/sl/%d/get' % self.loop, 'cycle_len', 'osc.udp://localhost:%s' % SERVER_PORT, '/cyclelen')
    liblo.send(self.target, '/sl/%d/get' % self.loop, 'loop_len', 'osc.udp://localhost:%s' % SERVER_PORT, '/looplen')
    liblo.send(self.target, '/sl/%d/get' % self.loop, 'loop_pos', 'osc.udp://localhost:%s' % SERVER_PORT, '/looppos')
    liblo.send(self.target, '/sl/%d/get' % self.loop, 'wet', 'osc.udp://localhost:%s' % SERVER_PORT, '/loopvelocity')

  def looppos_callback(self, path, args):
    loopnumber, looppos, position = args
    log("received '%s' message with arguments: %d, %s, %f" % (path, loopnumber, looppos, position))
    self.emitter.emitM('looppos', looppos)
                                                                                                               
  def loopcount_callback(self, path, args):
    hosturl, version, loopcount = args
    log("received '%s' message with arguments: %s, %s, %d" % (path, hosturl, version, loopcount))
    self.emitter.emitM('loopcount', loopcount)
                                                                                                               
  def loopstate_callback(self, path, args):
    loopnumber, state, value = args
    log("received '%s' message with arguments: %s, %s, %f" % (path, loopnumber, state, value))
    self.emitter.emitM('loopstate', state)
                                                                                                               
  def loopvelocity_callback(self, path, args):
    loopnumber, control, value = args
    log("received '%s' message with arguments: %d, %s, %f" % (path, loopnumber, control, value))
    self.emitter.emitM('loopvelocity', value) 
                                                                                                               
  def fallback(self, path, args):
    a, b, c = args
    log("received unknown message '%s' %s:(%s) %s:(%s) %s:(%s) " % (path, a, type(a), b, type(b), c, type(c)))
    self.emitter.emitM('unknown', str("unknown message '%s' %s:(%s) %s:(%s) %s:(%s) " % (path, a, type(a), b, type(b), c, type(c))))

  def startOscServer(self):
    self.server.add_method('/looppos', 'isf', self.looppos_callback)
    self.server.add_method('/loopcount', 'ssi', self.loopcount_callback)
    self.server.add_method('/loopstate', 'isf', self.loopstate_callback)
    self.server.add_method('/loopvelocity', 'isf', self.loopvelocity_callback)
    self.server.add_method(None, None, self.fallback)
    while True:
      self.server.recv(100)

osc_server = OscSooperLooper()
osc_server.start()
