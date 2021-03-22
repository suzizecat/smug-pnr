from structure.geometry import Segment, Point
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

	def have_crossing_with(self,other : Net):
		if other in self.netlist :
			raise RuntimeError

		ret = 0
		for net in self.valid_nets:
			if other.intersect_with(net):
				ret += 1
		return ret

	def ripup_pass(self):
		self.cleanup()
		self.compute_crossings()
		crossing_nets = sorted([n for n in self.valid_nets if len(n.crossings) > 0], key=lambda x: len(x.crossings),
							   reverse=True)
		new_nets = list()
		while(len(crossing_nets) > 0) :

			net = crossing_nets[0]
			crossing_match = net.crossings[0]
			crs_strt_pt = crossing_match.start - Point(crossing_match.x,crossing_match.y) * 0.05
			poss1 = (Net(net.start, crs_strt_pt) ,Net(crs_strt_pt,net.end))

			crs_end_pt = crossing_match.end  + Point(crossing_match.x,crossing_match.y) * 0.05
			poss2 = (Net(net.start, crs_end_pt), Net(crs_end_pt, net.end))

			poss1_crosses = self.have_crossing_with(poss1[0]) + self.have_crossing_with(poss1[1])
			poss2_crosses = self.have_crossing_with(poss2[0]) + self.have_crossing_with(poss2[1])

			if poss1_crosses == poss2_crosses :
				len_poss1 = poss1[0].sqlength + poss1[1].sqlength
				len_poss2 = poss2[0].sqlength + poss2[1].sqlength
				selected_path = poss1 if len_poss1 < len_poss2 else poss2
			else :
				print("Rip-up on less crossings")
				selected_path = poss1 if poss1_crosses < poss2_crosses else poss2

			new_nets.extend(selected_path)
			net.invalid = True
			net.clear_crossing()

			crossing_nets = sorted([n for n in self.valid_nets if len(n.crossings) > 0], key=lambda x: len(x.crossings),
								   reverse=True)

		self.netlist.extend(new_nets)

	def cleanup_colinear(self):
		temp_netlist = self.netlist
		temp_prev_netlist = None
		print("Cleanup colinear...")
		while temp_netlist is not None :
			temp_prev_netlist = temp_netlist
			temp_netlist = self._cleanup_one_colinear(temp_netlist)

		self.netlist = temp_prev_netlist

	def _cleanup_one_colinear(self,temp_netlist):
		to_skip = list()
		edited_netlist = temp_netlist
		run_again = False
		for net in edited_netlist :
			for other in [x for x in edited_netlist if x not in to_skip] :
				if other is net :
					continue
				if net.coef != other.coef :
					continue
				# On est parallèles
				if net.end == other.start :
					lookup_node = net.end
					sharings = [x for x in edited_netlist if (x not in to_skip and x is not net and x is not other and (x.start == lookup_node or x.end == lookup_node))]
					if len(sharings) == 0 :
						edited_netlist.remove(net)
						edited_netlist.remove(other)
						edited_netlist.append(Net(net.start,other.end))
						run_again = True
			to_skip.append(net)

		return temp_netlist if run_again else None

	def cleanup(self) :
		self.reset_crossings()
		self.netlist = self.valid_nets
		self.cleanup_colinear()









