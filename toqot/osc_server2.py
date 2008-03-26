#!/usr/bin/env python

import liblo
import sys

try:
  server = liblo.Server(1234)
except liblo.ServerError, err:
  print str(err)
  sys.exit()

def looppos_callback(path, args):
  loopnumber, loop_pos, position = args
  print "received '%s' message with arguments: %d, %s, %f" % (path, loopnumber, loop_pos, position)
                                                                                                               
def loopcount_callback(path, args):
  hosturl, version, loopcount = args
  print "received '%s' message with arguments: %s, %s, %d" % (path, hosturl, version, loopcount)
                                                                                                               
def loopstate_callback(path, args):
  loopnumber, state, value = args
  print "received '%s' message with arguments: %s, %s, %f" % (path, loopnumber, state, value)
                                                                                                               
def loopvelocity_callback(path, args):
  loopnumber, control, value = args
  print "received '%s' message with arguments: %d, %s, %f" % (path, loopnumber, control, value)
                                                                                                               
def fallback(path, args):
  a, b, c = args
  print "received unknown message '%s' %s:(%s) %s:(%s) %s:(%s) " % (path, a, type(a), b, type(b), c, type(c))

server.add_method('/looppos', 'isf', looppos_callback)
server.add_method('/loopcount', 'ssi', loopcount_callback)
server.add_method('/loopstate', 'isf', loopstate_callback)
server.add_method('/loopvelocity', 'isf', loopvelocity_callback)
server.add_method(None, None, fallback)

while True:
  server.recv(100)

"""test in ipython:
import liblo

target = liblo.Address(9951)
liblo.send(target, '/sl/0/register_auto_update', 'loop_pos', 100, 'osc.udp://localhost:1234', '/looppos')
liblo.send(target, '/ping', 'osc.udp://localhost:1234', '/loopcount')
liblo.send(target, '/sl/0/get', 'state', 'osc.udp://localhost:1234', '/loopstate')
liblo.send(target, '/sl/0/register_auto_update', 'wet', 100, 'osc.udp://localhost:1234', '/loopvelocity')
"""
