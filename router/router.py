from structure.geometry import Segment
import typing as T

class Net(Segment):
	def __init__(self,start = None, end = None ):
		super().__init__(start,end)
		self.invalid = False
		self.crossings : T.List[Net] = list()


	@property
	def manhattan(self) -> T.Union [T.Tuple["Net"],T.Tuple["Net" ,"Net","Net"]]:
		return tuple([Net(x.start,x.end) for x in super().manhattan])

	def add_crossing(self,other : "Net"):
		if other not in self.crossings :
			self.crossings.append(other)
			other.add_crossing(self)

	def clear_crossing(self):
		for c in self.crossings :
			c.crossings.remove(self)
		self.crossings.clear()


class Router :
	def __init__(self, netlist):
		self.netlist : T.List[Net] = netlist
		self.overlaps = 0

	def compute_crossings(self):
		self.reset_crossings()

		net_done = list()
		self.overlaps = 0
		for curr_net in [x for x in self.netlist if not x.invalid]:
			self.compute_net_crossings(curr_net,local_reset=False, skiplist=net_done)
			net_done.append(curr_net)

	def compute_net_crossings(self, net : Net, local_reset = True, skiplist : T.List[Net] = None):
		net_done = skiplist if skiplist is not None else list()
		if local_reset :
			if len(net.crossings) > 0 :
				self.overlaps -= len(net.crossings)
				net.clear_crossing()

		for other_net in [x for x in self.netlist if (x not in net_done and x is not net and not x.invalid)]:
			if net.intersect_with(other_net):
				net.add_crossing(other_net)
				self.overlaps += 1

	def reset_crossings(self):
		for n in self.netlist:
			n.clear_crossing()

	@property
	def valid_nets(self):
		return [n for n in self.netlist if not n.invalid]

	def process_manhattan(self):
		new_wires = list()
		w : Net
		for w in self.valid_nets :
			w.invalid = True
			new_wires.append(w)
			new_wires.extend(w.manhattan)
		self.netlist = new_wires

	def ripup_pass(self):
		self.cleanup()
		self.compute_crossings()
		crossing_nets = sorted([n for n in self.valid_nets if len(n.crossings) > 0], key=lambda x: len(x.crossings),
							   reverse=True)
		new_nets = list()
		while(len(crossing_nets) > 0) :

			net = crossing_nets[0]
			crossing_match = net.crossings[0]
			poss1 = (Net(net.start,crossing_match.start),Net(crossing_match.start,net.end))
			len_poss1 = poss1[0].sqlength + poss1[1].sqlength
			poss2 = (Net(net.start, crossing_match.end), Net(crossing_match.end, net.end))
			len_poss2 = poss2[0].sqlength + poss2[1].sqlength

			selected_path = poss1 if len_poss1 < len_poss2 else poss2
			new_nets.extend(selected_path)
			net.invalid = True
			net.clear_crossing()

			crossing_nets = sorted([n for n in self.valid_nets if len(n.crossings) > 0], key=lambda x: len(x.crossings),
								   reverse=True)

		self.netlist.extend(new_nets)


	def cleanup(self) :
		self.netlist = self.valid_nets
		duplicate_to_remove : T.List[Net] = list()
		for n in self.netlist :
			for others in [x for x in self.netlist if x is not n and x not in duplicate_to_remove] :
				if n == others :
					duplicate_to_remove.append(n)
					break



