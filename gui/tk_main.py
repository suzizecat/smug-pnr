from tkinter import *
from tkinter.ttk import *
import typing as T
import structure.geometry as G

class MainWindow(Tk):
	def __init__(self, text : str = "Top", **kwargs):
		super().__init__()
		root = Frame(self)
		menubar = Menu(self)
		self["menu"] = menubar
		menu_action = Menu(menubar,tearoff=False)
		menubar.add_cascade(label="Actions",menu=menu_action)
		menu_action.add_command(label="Redraw",command=self.on_redraw)
		menu_action.add_separator()
		menu_action.add_command(label="800x600",command=lambda : self.on_resize("800x600"))
		menu_action.add_command(label="480x360",command=lambda : self.on_resize("480x360"))
		self.canvas = Canvas(root)
		self.canvas.configure(scrollregion=(0, 0, 800, 600))

		self.canvas.pack(fill=BOTH,side=TOP,expand=True)

		#btn = Button(root,text="toto")
		#btn.pack(fill=BOTH)
		#self.geometry("800x600")
		self.title("SMUG Router")
		root.pack(fill=BOTH,expand=True)


		self.wires : T.List[G.Segment] = list()
		p1 = G.Point(5,10)
		p2 = G.Point(650,300)
		s = G.Segment(p1,p2)
		self.wires.extend(s.manhattan)

		#self.minsize(100,100)
	def on_redraw(self):
		print("redraw")
		self.canvas.delete("all")
		self.canvas.create_rectangle(0,0,800,600,fill="#595")

		node_done = list()

		for s in self.wires :
			self.canvas.create_line(s.start.x,s.start.y,s.end.x,s.end.y,fill="#000")
			if s.start not in node_done :
				node_done.append(s.start)
			if s.end not in node_done :
				node_done.append(s.end)

		for node in node_done :
			self.canvas.create_oval(node.x-2,node.y-2,node.x+2,node.y+2,fill= "#0F0")
		print("done")


	def on_resize(self,new_geometry):
		self.geometry(new_geometry)
