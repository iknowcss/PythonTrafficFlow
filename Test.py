from Lane import Lane

vmax = 10
p = 0

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

l = Lane(vmax,p,initial_conditions)
print l.get_lane_bit_state()
print l.get_lane_velocity_state()
