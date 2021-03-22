import typing as T

class Point:
	def __init__(self, x = None, y = None):
		self.x = x
		self.y = y

	@property
	def is_valid(self):
		return self.y is not None and self.x is not None

	@staticmethod
	def orientation(a,b,c):
		"""
		Gives the orientation of a point triplet.
		:param a:
		:param b:
		:param c:
		:return: 1 if clockwise, 0 if colinear, -1 if counter-clockwise
		"""

		#On prends A comme origine.
		v1 = Point(b.x-a.x,b.y-a.y)
		v2 = Point(c.x-a.x,c.y-a.y)

		# On calcule le produit mixte entre v1 et v2, comme si on était en base orthonormée avec un troisième vecteur (0,0,1)
		# Si le produit est positif, on est en sens trigo, si c'est 0 on est colinéaire, si c'est négatif on est horaire

		sens = v1.x * v2.y - v1.y * v2.x

		if sens < 0 :
			return 1
		if sens > 0 :
			return -1
		return 0

	def __add__(self, other):
		if isinstance(other,Point):
			return Point(self.x + other.x, self.y + other.y)
		else :
			raise TypeError

	def __sub__(self, other):
		if isinstance(other,Point):
			return Point(self.x - other.x, self.y - other.y)
		else :
			raise TypeError

	def __mul__(self, other):
		return Point(self.x * other, self.y * other)

	def __str__(self):
		return f"({self.x:4d};{self.y:4d})"

	def __eq__(self, other : "Point"):
		return (self.x,self.y) == (other.x,other.y)



class Segment:
	def __init__(self, start : Point = None, end : Point = None):
		self.start = start
		self.end = end

	def __str__(self):
		return f"<{str(self.start)} -> {str(self.end)}>"

	@property
	def is_valid(self):
		ret = self.start is not None and self.end is not None
		ret &= self.start.is_valid and self.end.is_valid
		return ret

	def share_end_with(self,other: "Segment") -> int:
		ret = 0
		if self.start == other.start:
			ret += 1
		if self.start == other.end:
			ret += 1
		if self.end == other.start:
			ret += 1
		if self.end == other.end:
			ret += 1

		return ret

	@property
	def sqlength(self):
		return self.x **2 + self.y ** 2

	def __eq__(self, other : "Segment"):
		return (self.start,self.end) == (other.start,other.end) or (self.start,self.end) == (other.end,other.start)

	def intersect_with(self,other : "Segment", strict=False):

		if not strict and self.share_end_with(other) == 1 :
			return False

		o1 = Point.orientation(self.start, self.end,other.start)
		o2 = Point.orientation(self.start, self.end, other.end)
		o3 = Point.orientation(other.start, other.end, self.start)
		o4 = Point.orientation(other.start, other.end, self.end)

		#If we are not colinear
		if (o1 != o2) and (o3 != o4) :
			return True

		#If we have some colinearity,
		if o1 == 0 and other.start in self :
			return True
		if o2 == 0 and other.end in self :
			return True
		if o3 == 0 and self.start in other :
			return True
		if o4 == 0 and self.end in other :
			return True

		return False

	def __contains__(self, item):
		if isinstance(item,Point) :
			if ((item.x <= max(self.start.x, self.end.x)) and (item.x >= min(self.start.x, self.end.x)) and
					(item.y <= max(self.start.y, self.end.y)) and (item.y >= min(self.start.y, self.end.y))):
				return True
			return False
		raise TypeError


	@property
	def x(self):
		return self.end.x - self.start.x

	@property
	def y(self):
		return self.end.y - self.start.y

	@property
	def manhattan(self) -> T.Union [T.Tuple["Segment"],T.Tuple["Segment" ,"Segment","Segment"]]:
		if self.start.x == self.end.x or self.start.y == self.end.y:
			return tuple([self])

		facteur = (self.end.y - self.start.y) / (self.end.x - self.start.x)

		ret = []
		# Major horizontal component, we'll go H then V then H
		if abs(facteur) < 1 :
			first_end = Point(round(self.x / 2),0) + self.start
			second_end = Point(first_end.x,self.end.y)
		else:
			first_end = Point(0, round(self.y / 2)) + self.start
			second_end = Point(self.end.x, first_end.y)

		ret.append(Segment(self.start,first_end))
		ret.append(Segment(first_end,second_end))
		ret.append(Segment(second_end,self.end))

		return  tuple(ret)



if __file__ == "__main__" :
	p1 = Point(0,0)
	p2 = Point(10,5)
	seg = Segment(p1,p2)
	t = seg.manhattan

