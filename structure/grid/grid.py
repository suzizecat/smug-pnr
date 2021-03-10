import typing as T
from .node import GridNode


class Grid:
	def __init__(self):
		self.origin_x = 0
		self.origin_y = 0

		self.nodes : T.List[GridNode] = list()

	def add_node(self,n : GridNode):
		if n.parent_grid is self :
			return
		if n.parent_grid is not None :
			raise RuntimeError("Node already in a grid")
		self.nodes.append(n)
		n.parent_grid = self


