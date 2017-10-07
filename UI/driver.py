from Tkinter import *

class Application(Frame):

    def calibration(self):
        pass

    def end_calibration(self):
        pass

    def run(self):
        pass

    def end_run(self):
        pass

    def createWidgets(self):
        self.calibrate = Button(self)
        self.calibrate["text"] = "Calibrate",
        self.calibrate["command"] = self.calibration

        self.calibrate.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()


