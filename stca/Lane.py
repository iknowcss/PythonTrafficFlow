from Car import Car

class Lane:
	# Constructor
	def __init__(self,vmax,p,initial_lane_conditions):
		self.__lane_bit_state = [False] * len(initial_lane_conditions)
		self.__cars = list()
		
		position = 0
		last_car = None
		for velocity in initial_lane_conditions:
			if velocity is None or velocity < 0:
				self.__lane_bit_state[position] = False
			else:
				self.__lane_bit_state[position] = True
				car = Car(position,velocity,vmax,p,self.__lane_bit_state)
				if last_car is not None:
					last_car.set_next_car(car)
				last_car = car
				
			position += 1
	
	# Private methods
	def __calc_new_velocities(self):
                for car in __cars:
                        car.calc_new_velocity()
	
	def __move_cars(self):
		for car in __cars:
                        car.move()
		
	def __remove_last_car(self):
		for car in __cars:
                        car.get__position()
                        if car.__position == len(__lane_bit_state - 1):    # If car's position is at the last value of the lane bit state, we want to remove it
                                # The -1 is at the end of __lane_bit_state because I believe
                                # car.__position starts at 0,1,2,...but len will give the length starting from 1. 
                                del Lane.__cars[-1]
                                __lane_bit_state[-1] = False # Now that car is gone so we want to change that value to False
                                car.set_next_car(None) #I dont think this is going to work like this cause I think this goes forward but we want it to go back a car?
                                
                                 
                        
	
	# Public methods
	def step(self):
		"""TODO: implement Lane#step()"""
		return self.get_lane_bit_state()
	
	def get_lane_bit_state(self):
		return list(self.__lane_bit_state)
        
        def get_lane_velocity_state(self):
                lcl = []  #lane condition list is empty to start
                ci = 0   #Specify this so that below we start by pulling the zeroth car from the car list (the first car)
                for bit_state in __lane_bit_state:
                        if bit_state == True:
                                lcl.append(__cars[ci].get_velocity())  #if true, we add the cars velocity to the list
                                ci += 1  #add so that next time it selects the next car in the list of cars
                        else:
                                lcl.append(None)  #if false, we add None
