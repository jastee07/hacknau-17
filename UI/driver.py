import matplotlib
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

class GUI:

    def destroy(e):
        sys.exit()

    root = Tk.Tk()
    root.wm_title("Heartbeat Monitor")


    f = Figure(figsize=(5, 4), dpi=100)
    a = f.add_subplot(111)
    t = arange(0.0, 3.0, 0.01)
    s = sin(2*pi*t)

    a.plot(t, s)
    a.set_title('Heartbeat Monitor')
    a.set_xlabel('Time')
    a.set_ylabel('Beats per Minute')


    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    calibrate_button = Tk.Button(master=root, text='Calibrate', command=sys.exit)
    calibrate_button.pack(side=Tk.BOTTOM)

    Tk.mainloop()

root = Tk()
gui = GUI(master=root)
root.mainloop()
