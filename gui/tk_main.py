from tkinter import *
from tkinter.ttk import *

from structure.grid import Grid as SMUGGrid

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

		self.nodes_grid = SMUGGrid()
		self.nodes_grid.origin_x = 5
		self.nodes_grid.origin_y = 5
		self.nodes_grid.build_grid(20,20,40,30, diag=True)
		self.nodes_grid.route_path(self.nodes_grid.grid[2][3],self.nodes_grid.grid[35][22])


		#self.minsize(100,100)
	def on_redraw(self):
		print("redraw")
		self.canvas.delete("all")
		self.canvas.create_rectangle(0,0,800,600,fill="#595")

		node_done = list()
		for node in self.nodes_grid.nodes :
			for n in node.neighbors :
				self.canvas.create_line(node.position_x,node.position_y,n.position_x,n.position_y,fill="#333")
				node_done.append(node)
		for node in self.nodes_grid.nodes :
			self.canvas.create_oval(node.position_x-2,node.position_y-2,node.position_x+2,node.position_y+2,fill="#b00" if not node.routed else "#0F0")
		print("done")


	def on_resize(self,new_geometry):
		self.geometry(new_geometry)
