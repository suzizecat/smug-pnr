from structure.geometry import Point
from router import Net
import typing as T

def read_design() -> T.List[Net] :
	p1 = Point(15,15)
	p2 = Point(750,400)

	p3 = Point(350,50)
	p4 = Point(450,550)

	p5 = Point(20,500)
	p6 = Point(780,300)

	p7 = Point(400, 80)
	p8 = Point(500, 500)

	ret = list()
	ret.append(Net(p1,p2))
	ret.append(Net(p3,p4))
	ret.append(Net(p5,p6))
	ret.append(Net(p7,p8))



	return ret