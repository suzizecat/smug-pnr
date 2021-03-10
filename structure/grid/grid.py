import typing as T
from .node import GridNode


class Grid:
	def __init__(self):
		self.origin_x = 0
		self.origin_y = 0

		self.nodes : T.List[GridNode] = list()
		self.grid : T.List[T.List[GridNode]] = list()

	def add_node(self,n : GridNode):
		if n.parent_grid is self :
			return
		if n.parent_grid is not None :
			raise RuntimeError("Node already in a grid")
		self.nodes.append(n)
		n.parent_grid = self

	def build_grid(self,x_step,y_step,x,y):
		self.grid.clear()
		for i in range(x) :
			self.grid.append(list())
			for j in range(y):
				self.add_node(GridNode(i*x_step + self.origin_x,j*y_step + self.origin_y))
				self.grid[-1].append(self.nodes[-1])

		for i in range(x) :
			for j in range(y) :
				node = self.grid[i][j]
				for k in range(i-1,i+2) :
					for l in range(j-1,j+2) :
						if (i,j) == (k,l) or k < 0 or l < 0 or k >= len(self.grid)  or l >= len(self.grid[k]):
							continue
						node.add_neighbors(self.grid[k][l])

