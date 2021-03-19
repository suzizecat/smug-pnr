from structure.geometry import Segment
import typing as T

class Net(Segment):
	def __init__(self,start = None, end = None ):
		super().__init__(start,end)

		self.crossings_nb : T.List[Net] = list()

class Router :
	def __init__(self, netlist):
		self.netlist : T.List[Segment] = netlist

