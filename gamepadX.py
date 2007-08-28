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

import thread, sys, time
import xAction

def runGamepadX():
    global nomo_state
    try:
        while 1:
            for i in konf:
                if getattr(K,i[1])(i[2]) != 0:
                    keep = True

            if K.jsd.update() or keep == True:
                keep = False
                K.moveMouse()
                for i,iobj in enumerate(konf):
                    for j in iobj[0]:
                        if getattr(K, j[0])(j[1]) == 1:
                            nomo_state += 1
                
                    if nomo_state == len(konf[i][0]):
                        nomo_state = 0
                        getattr(K, konf[i][3])(getattr(K, konf[i][1])(konf[i][2]),konf[i][1]+str(konf[i][2]))
                    else:
                        nomo_state = 0

            sys.stdout.flush()
            time.sleep(0.02)
        
    except KeyboardInterrupt:
        print
        sys.exit()

konf = [        [[['bt',7]], 'ax', 4, 'backspaceDeleteAx'],
                [[['bt',7]], 'ax', 5, 'enterEscapeAx'],
                [[], 'ax', 2, 'setMouseX'],
                [[], 'ax', 3, 'setMouseY'],
                [[], 'bt', 4, 'leftClick'],
                [[], 'bt', 6, 'rightClick'],
                [[], 'bt', 5, 'middleClick'],
                [[], 'ax', 5, 'arrowUpDownAx'],
                [[], 'ax', 4, 'arrowLeftRightAx']
                ]
nomo_state = None
K = None

def run():
    global K, nomo_state
    K = XAction.XAction()
    K.getMouseCoord()
    nomo_state = 0
    
    thread.start_new_thread(runGamepadX, ())
