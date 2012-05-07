from util.test import *
from stca.Car import Car

# Car parameters
vmax = 5
p = 0
lane_bit_state_ref = [\
	False,False,False,True,False,False,True,True,\
	False,True,False,True,True,False,False,False\
]

# Car 1
c1_position = 3
c1_velocity = 1
c1 = Car(c1_position,c1_velocity,vmax,p,lane_bit_state_ref)

# Car 2
c2_position = 6
c2_velocity = 1
c2 = Car(c2_position,c2_velocity,vmax,p,lane_bit_state_ref)

print "Testing the Car class"

print "- Car#get_position():",
run_test(\
	c1.get_position() == c1_position and\
	c2.get_position() == c2_position,\
	"Ok",\
	"Did not return the correct position"
)

print "- Car#set_next_car(car):",
c1.set_next_car(c1)
run_test(\
	c1.get_next_car() is c2,\
	"Ok",
	"get_next_car() did not return the next car after it was set"\
)
