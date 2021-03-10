from tkinter import *
from tkinter.ttk import *

class MainWindows(Toplevel):
	def __init__(self, master = None,text : str = "Please wait", **kwargs):
		super().__init__(master, kwargs)
		menubar = Menu(self)
		menu_action = Menu(menubar)
		menu_action.add_command(label="Redraw",command=self.on_redraw)

		menubar.add_cascade("Actions",menu_action)

		self.minsize(100,100)

	def on_redraw(self):
		print("redraw")
