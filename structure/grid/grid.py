import typing as T
from .node import GridNode
import math

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

	def build_grid(self,x_step,y_step,x,y,diag= False):
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
						if not diag and (i != k and j != l) :
							continue
						node.add_neighbors(self.grid[k][l])

	def route_path(self,origin : GridNode, dest : GridNode):
		eucl_dist = lambda x : (dest.position_x-x.position_x)**2  + (dest.position_y-x.position_y)**2
		path = list()
		path.append(origin)

		curr_node = origin
		while curr_node != dest:
			curr_node.routed = True
			curr_dist = eucl_dist(curr_node)
			smalest_dist = curr_dist
			next_node = curr_node
			for node in curr_node.neighbors :
				if eucl_dist(node) < smalest_dist :
					next_node = node
					smalest_dist = eucl_dist(node)
			if next_node == curr_node :
				raise RuntimeError("Route exception")
			else :
				path.append(next_node)
				curr_node = next_node

		curr_node.routed = True




