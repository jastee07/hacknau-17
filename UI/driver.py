from Tkinter import *


class Application(Frame):
    calibrating = False
    running = False

    def start_calibration(self):
        self.calibrate.config(text="Quit Calibrating", command=self.end_calibration)
        self.calibrating = True

    def end_calibration(self):
        self.calibrate.config(text="Calibrate", command=self.start_calibration)
        self.calibrating = False

    def start_run(self):
        self.run.config(text="Quit Running", command=self.end_run)
        self.running = True

    def end_run(self):
        self.run.config(text="Run", command=self.start_run)
        self.running = False

    def create_widgets(self):
        button_height = 2
        button_width = 14
        self.calibrate = Button(self)
        self.calibrate["text"] = "Calibrate"
        self.calibrate["command"] = self.start_calibration
        self.calibrate.pack({"side": "left"})
        self.calibrate.config(height=button_height, width=button_width)

        self.run = Button(self)
        self.run["text"] = "Run"
        self.run["command"] = self.start_run
        self.run.pack({"side": "right"})
        self.run.config(height=button_height, width=button_width)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

root = Tk()
app = Application(master=root)
app.mainloop()


