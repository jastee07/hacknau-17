from Tkinter import *


class Application(Frame):
    calibrating = False
    def start_calibration(self):
        self.calibrate.config(text="Quit Calibration", command=self.end_calibration)

    def end_calibration(self):
        self.calibrate.config(text="Calibrate", command=self.start_calibration)

    def start_run(self):
        pass

    def end_run(self):
        pass

    def createWidgets(self):
        self.calibrate = Button(self)
        self.calibrate["text"] = "Calibrate"
        self.calibrate["command"] = self.start_calibration
        self.calibrate.pack({"side": "left"})

        self.run = Button(self)
        self.run["text"] = "Run"
        self.calibrate["command"] = self.start_run
        self.run.pack({"side": "right"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()


