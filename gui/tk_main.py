from tkinter import *
from tkinter.ttk import *
import typing as T
import structure.geometry as G
from router import Router
from design import read_design
class MainWindow(Tk):
	def __init__(self, text : str = "Top", **kwargs):
		super().__init__()
		root = Frame(self)
		menubar = Menu(self)
		self["menu"] = menubar
		#menu_action = Menu(menubar,tearoff=False)
		#menubar.add_cascade(label="Actions",menu=menu_action)
		menubar.add_command(label="Stats", command=self.on_stats)
		menubar.add_command(label="Redraw",command=self.on_redraw)
		menubar.add_command(label="Ripup",command=self.on_ripup)
		menubar.add_command(label="Manhattan", command=self.on_manhattan)
		menubar.add_command(label="Reset",command=self.on_reset)
		menubar.add_command(label="Cleanup", command=self.on_cleanup)
		self.canvas = Canvas(root)
		self.canvas.configure(scrollregion=(0, 0, 800, 600))

		self.canvas.pack(fill=BOTH,side=TOP,expand=True)

		#btn = Button(root,text="toto")
		#btn.pack(fill=BOTH)
		#self.geometry("800x600")
		self.title("SMUG Router")
		root.pack(fill=BOTH,expand=True)
		self.router: Router = Router(read_design())
		self.on_reset()

	def on_reset(self):
		self.router = Router(read_design())
		self.on_redraw()
		self.on_resize("800x600")

	#self.minsize(100,100)
	def on_redraw(self):
		print("redraw")
		self.canvas.delete("all")
		self.canvas.create_rectangle(0,0,800,600,fill="#595")

		node_done = list()

		for s in self.router.netlist :
			self.canvas.create_line(s.start.x,s.start.y,s.end.x,s.end.y,fill="#000" if not s.invalid else "#755",dash=None if not s.invalid else (5,) )
			if s.start not in node_done :
				node_done.append(s.start)
			if s.end not in node_done :
				node_done.append(s.end)

		for node in node_done :
			self.canvas.create_oval(node.x-2,node.y-2,node.x+2,node.y+2,fill= "#0F0")
		print("\tdone")

	def on_manhattan(self):
		self.router.process_manhattan()
		self.on_redraw()

	def on_ripup(self):
		self.router.ripup_pass()
		self.on_redraw()

	def on_resize(self,new_geometry):
		self.geometry(new_geometry)

	def on_stats(self):
		self.router.compute_crossings()
		print(f"Found {self.router.overlaps} overlaps")

	def on_cleanup(self):
		self.router.cleanup()
		self.on_redraw()