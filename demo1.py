from ui.LaneDisplay import LaneDisplay
from stca.Lane import Lane as STCALane
from rule184.Lane import Lane as CALane

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
#lane = STCALane(1,0,ilc)
#ld = LaneDisplay(lane)
#ld.step()

initial_bit_state = "001000100001100100001010011000111"
#initial_bit_state = "0000000000000000000000000000001000000000000000000000000000000"
ca_lane = CALane(initial_bit_state)
ca_lane_display = LaneDisplay(ca_lane,50)
