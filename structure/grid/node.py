import typing as T

class GridNode:
	def __init__(self, x : int,y : int):
		self.neighbors : T.List[GridNode] = list()
		self.position_x: int = x
		self.position_y: int = y

		self.parent_grid = None

	def add_neighbors(self, other : "GridNode"):
		if other not in self.neighbors :
			self.neighbors.append(other)
			other.add_neighbors(self)
