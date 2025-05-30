import os
import sys
import gdb

class MyBreakpoint (gdb.Breakpoint):
    def __init__(self, pos, predicate, handler):
        gdb.Breakpoint.__init__(self, pos)
        self.pos = pos
        self.predicate = predicate
        self.handler = handler

    def stop (self):
        return self.predicate(self)

def setup():
    print('Running GDB from: %s\n'%(gdb.PYTHONDIR))
    gdb.execute("set pagination off")
    gdb.execute("set print pretty")
    gdb.execute("define hook-quit\nset confirm off\nend")
    print('Setup complete !!\n')

def registerBreakpoint(breakpoints):
    for bp in breakpoints:
        def stopHandler(event):
            if event.breakpoint.location == bp.pos:
                bp.handler(bp)
                gdb.execute("c")
        gdb.events.stop.connect(stopHandler)