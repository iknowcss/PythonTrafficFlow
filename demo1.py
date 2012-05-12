from ui.LaneDisplay import LaneDisplay
from stca.Lane import Lane

ilc = [\
	None,\
	0,\
	1,\
	None,\
	None,\
	1,\
	None,\
	1,\
	None,\
	1\
]
lane = Lane(1,0,ilc)
ld = LaneDisplay(lane)
