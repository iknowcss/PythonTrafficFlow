from util.test import *
from stca.Lane import Lane

# Lane parameters
vmax = 10
p = 0

# Initial conditions
# 00010011 01011000
initial_conditions = list()
initial_conditions.append(None)
initial_conditions.append(None)
initial_conditions.append(None)
initial_conditions.append(5)
initial_conditions.append(None)
initial_conditions.append(None)
initial_conditions.append(4)
initial_conditions.append(3)
initial_conditions.append(None)
initial_conditions.append(2)
initial_conditions.append(None)
initial_conditions.append(1)
initial_conditions.append(0)
initial_conditions.append(None)
initial_conditions.append(None)
initial_conditions.append(None)

ic_copy = list(initial_conditions)

print "Testing the Lane class"
l = Lane(vmax,p,initial_conditions)

print "- Lane#get_lane_bit_state:",
run_test(l.get_lane_bit_state() == [\
	False,False,False,True,False,False,True,True,\
	False,True,False,True,True,False,False,False\
],"Ok","The lane bit state returned was incorrect")

print "- Lane#get_lane_velocity_state():",
lvs = l.get_lane_velocity_state()
run_test(lvs == ic_copy,"Ok",\
	"The lane velocity state returned was incorrect.\n" + \
	"  Function returned\n  " + str(lvs) + "\n" + \
	"  Should be\n  " + str(ic_copy)\
)

