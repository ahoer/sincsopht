import os
import tkinter
from myapp import MyApp
from systemdata import SystemData
from filelogger import FileLogger

__author__ = 'fernass daoud'

parameters = SystemData()
parameters.commandline()

if not parameters.nogui:
    root = tkinter.Tk()
    app = MyApp(parameters, root)
    app.mainloop()
else:
    log = FileLogger(parameters.verbose)
    parameters.run(log)
