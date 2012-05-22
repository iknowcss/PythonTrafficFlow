from ui.LaneLoader import LaneLoader
from stca.Lane import Lane as STCALane
from rule184.Lane import Lane as Rule184Lane

LaneLoader({
	"stca": STCALane,
	"rule184": Rule184Lane
})