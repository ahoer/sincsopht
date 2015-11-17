import logging
import time
import tkinter as tk

class WidgetLogger(logging.Handler):
    def __init__(self, widget, verbose):
        logging.Handler.__init__(self)
        self.verbose = verbose
#        frm = logging.Formatter("[{levelname:8}], {asctime}: {message}", "%d.%m.%Y", style="{")
#        self.setFormatter(frm)
        self.setLevel(logging.INFO)
        self.widget = widget
        self.widget.config(state='disabled')

    def emit(self, record, parameters, tag=""):
        self.widget.config(state='normal')
        # Append message (record) to the widget
        if tag=="normal" and parameters.verbose:
            message = "[INFO    ]: " + time.strftime("%d.%m.%Y %H:%M:%S - ") + record
            self.widget.insert(tk.END, message + '\n', tag)
        elif tag=="warning":
            message = "[WARNING ]: " + time.strftime("%d.%m.%Y %H:%M:%S - ") + record
            self.widget.insert(tk.END, message + '\n', tag)
        elif tag=="error":
            message = "[ERROR   ]: " + time.strftime("%d.%m.%Y %H:%M:%S - ") + record
            self.widget.insert(tk.END, record + '\n', tag)
        elif tag=="success":
            message = "[SUCCESS   ]: " + time.strftime("%d.%m.%Y %H:%M:%S - ") + record
            self.widget.insert(tk.END, record + '\n', tag)
#        else:
#            self.widget.insert(tk.END, record + '\n', tag)

        self.widget.see(tk.END)  # Scroll to the bottom
        self.widget.config(state='disabled')
