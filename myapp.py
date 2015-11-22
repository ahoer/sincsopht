import tkinter
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk
from widgetlogger import WidgetLogger

__author__ = 'fernass daoud'


class MyApp(tkinter.Frame):
    def __init__(self, parameters, master=None):
        super().__init__(master)
        self.parameters = parameters

        self.font_main = tkfont.Font(family="Arial", size=10, weight="bold", slant="italic")
        self.fontlog = tkfont.Font(family="FixedSys", size=8)
#        master.resizable(width=False, height=True)
        master.geometry("970x500+200+100")


        self.directory_image = Image.open("./images/open-file-icon.png").resize((40,25))
        self.directory_image_tk = ImageTk.PhotoImage(self.directory_image)

#        master.geometry("{}x{}".format(800, 500))
#        master.minsize(width=500, height=500)
#        master.maxsize(width=500, height=500)

        self.grid()
        self.createWidget()
        self.createBindings()


###########################################
    def createWidget(self):
        self.SourceLabel = tkinter.Label(self, text="Source Directory")
        self.SourceLabel.grid(row=0, column=0, padx=5, pady=5)
        self.TargetLabel = tkinter.Label(self, text="Target Directory")
        self.TargetLabel.grid(row=1, column=0, padx=5, pady=5)
        self.SourceString = tkinter.StringVar(self, "Please choose source directory")
        self.TargetString = tkinter.StringVar(self, "Please choose target directory")
        self.SourceEntry = tkinter.Entry(self, textvariable=self.SourceString, width=75, font=self.font_main,
                                         insertbackground="red")
        self.SourceEntry.grid(row=0, column=1, padx=5, pady=5)
        self.TargetEntry = tkinter.Entry(self, textvariable=self.TargetString, width=75, font=self.font_main,
                                         insertbackground="red")
        self.TargetEntry.grid(row=1, column=1, padx=5, pady=5)

        self.SourceDirectory = tkinter.Button(self, image=self.directory_image_tk, command=self.sdHandler)
        self.SourceDirectory.grid(row=0, column=2, padx=5, pady=5)
        self.TargetDirectory = tkinter.Button(self, image=self.directory_image_tk, command=self.tdHandler)\
            .grid(row=1, column=2,padx=5,pady=5)
        self.Placeholder = tkinter.Label(self, text="", width=5).grid(row=0, column=3, columnspan=1, rowspan=1)
        self.SyncButton = tkinter.Button(self,
                                         text="Synchronisation",
                                         command=self.syncHandler,
                                         height=5,
                                         width=15,
                                         bg="#b7feea",
                                         relief="groove",
                                         borderwidth=5,
                                         cursor="pirate",
                                         activeforeground="white",
                                         activebackground="red")
        self.SyncButton.grid(row=0, column=4, rowspan=2, columnspan=2, padx=5, pady=5)
        self.Close = tkinter.Button(self,
                                    text="Close",
                                    width=15,
                                    command=self.close,
                                    relief="groove",
                                    borderwidth=5)
        self.Close.grid(row=2,column=4,columnspan=2, padx=5, pady=5)
# Checkbuttons
        self.BidirectCheck = tkinter.Checkbutton(self)
        self.BidirectBool = tkinter.BooleanVar(self, value=True)
        self.BidirectCheck["variable"] = self.BidirectBool
        self.BidirectCheck["text"] ="bidirectional"
        self.BidirectCheck["command"] = self.bidirectHandler
        self.BidirectCheck.grid(row=2, column=0, sticky="W")
        self.DeleteCheck = tkinter.Checkbutton(self)
        self.DeleteBool = tkinter.BooleanVar(self, value=False)
        self.DeleteCheck["variable"] = self.DeleteBool
        self.DeleteCheck["text"] ="delete"
        self.DeleteCheck["command"] = self.deleteHandler
        self.DeleteCheck.grid(row=3, column=0, sticky="W")
        self.ForceCheck = tkinter.Checkbutton(self)
        self.ForceBool = tkinter.BooleanVar(self, value=False)
        self.ForceCheck["variable"] = self.ForceBool
        self.ForceCheck["text"] ="force"
        self.ForceCheck["command"] = self.forceHandler
        self.ForceCheck.grid(row=4, column=0, sticky="W")

        self.VerboseCheck = tkinter.Checkbutton(self)
        self.VerboseBool = tkinter.BooleanVar(self, value=False)
        self.VerboseCheck["variable"] = self.VerboseBool
        self.VerboseCheck["text"] ="verbose"
        self.VerboseCheck["command"] = self.verboseHandler
        self.VerboseCheck.grid(row=5, column=0, sticky="W")

        self.LogText = tkinter.Text(self, wrap="word", height=15, font=self.fontlog, padx=5, pady=5)
        self.LogText.tag_config("normal", foreground="black")
        self.LogText.tag_config("warning", foreground="orange")
        self.LogText.tag_config("error", foreground="red")
        self.LogText.tag_config("success", foreground="green")
        self.LogText.tag_config("c", justify="center")
        self.LogText.tag_config("u", underline=True)
        self.LogText.tag_config("space_below", spacing3=25)

#        self.LogText.tag_config("ind", lmargin1=10)
        self.LogText.insert("end", "Welcome to SincSopht", ("c", "u", "space_below"))
        self.LogText.insert("end", "\n", "normal")
        self.LogText.configure(state="disable")
        self.LogText.grid(row=6, column=1, columnspan=1, rowspan=1, sticky="n"+"s"+"e"+"w")

        self.LogScrollY = tkinter.Scrollbar(self, relief="groove", orient="vertical")
        self.LogText["yscrollcommand"] = self.LogScrollY.set
#        self.LogScroll["command"] = self.LogText.yview
        self.LogScrollY["command"] = self.LogScrollYHandler
        self.LogScrollY.grid(row=6,column=2, sticky="n"+"s"+"w")

        self.LogScrollX = tkinter.Scrollbar(self, relief="groove", orient="horizontal")
        self.LogText["xscrollcommand"] = self.LogScrollX.set
#        self.LogScroll["command"] = self.LogText.yview
        self.LogScrollX["command"] = self.LogScrollXHandler
        self.LogScrollX.grid(row=7, column=1, sticky="n"+"e"+"w")

        self.LogWidget = WidgetLogger(self.LogText, self.parameters.verbose)

###########################################
    def createBindings(self):
        self.SyncButton.bind("<Shift-ButtonPress-1>", self.SyncShiftButton_1)

############## HANDLER ####################
    def syncHandler(self):
#        YES = messagebox.askyesno(title="It's getting serious!", message="Ready for Synchronisation")
#        if YES:
        self.parameters.source = self.SourceString.get()
        self.parameters.target = self.TargetString.get()
        self.parameters.bidirectional = self.BidirectBool.get()
        self.parameters.force = self.ForceBool.get()
        self.parameters.delete = self.DeleteBool.get()
        self.parameters.verbose = self.VerboseBool.get()

        self.parameters.run(self.LogWidget)

############## HANDLER ####################
    def SyncShiftButton_1(self, event):
        self.SyncButton["bg"] = "red"

############## HANDLER ####################
    def sdHandler(self):
        self.SourceDirectoryPath = filedialog.askdirectory(title="Choose The Path of Source Directory")
        self.SourceString.set(self.SourceDirectoryPath)
#        self.SourceEntry.select_range(0,"end")

############## HANDLER ####################
    def tdHandler(self):
        self.TargetDirectoryPath = filedialog.askdirectory(title="Choose The Path of Target Directory")
        self.TargetString.set(self.TargetDirectoryPath)

############## HANDLER ####################
    def close(self):
        self.quit()
############## HANDLER ####################
    def bidirectHandler(self):
        if self.BidirectBool:
            self.DeleteCheck.deselect()
            self.ForceCheck.deselect()
#            self.DeleteBool.set(False)
#            self.ForceBool.set(False)
############## HANDLER ####################
    def deleteHandler(self):
        if self.DeleteBool:
            self.BidirectCheck.deselect()
#            self.BidirectBool.set(False)
############## HANDLER ####################
    def forceHandler(self):
        if self.ForceBool:
            self.BidirectCheck.deselect()
############## HANDLER ####################
    def verboseHandler(self):
        pass
#            self.BidirectBool.set(False)
############## HANDLER ####################

    def LogScrollYHandler(self, *L):
        op, HowMany = L[0], L[1]
        if op == "scroll":
            units = L[2]
            self.LogText.yview_scroll(HowMany, units)
        elif op == "moveto":
            self.LogText.yview_moveto(HowMany)
############## HANDLER ####################

    def LogScrollXHandler(self, *L):
        op, HowMany = L[0], L[1]
        if op == "scroll":
            units = L[2]
            self.LogText.xview_scroll(HowMany, units)
        elif op == "moveto":
            self.LogText.xview_moveto(HowMany)
