from Car import Car

class Lane:
	## Constructor ##
	def __init__(self,vmax,p,initial_lane_conditions):
		# Initalize the Lane's instance variables
		self.__lane_length = len(initial_lane_conditions)
		self.__lane_bit_state = [False] * self.__lane_length
		self.__cars = list()
		self.__car_count = 0
		self.__step_count = 0
		self.__slowing_probability = p
		self.__max_velocity = vmax
	
		# Parse initial_lane_conditions and build and preare the cars and 
		# car array
		head_car = None # The car farthest to the left
		previous_car = None
		position = 0
		for velocity in initial_lane_conditions:
			if velocity is None or velocity < 0:
				self.__lane_bit_state[position] = False
			else:
				self.__lane_bit_state[position] = True
				
				# Ensure the velocities
				if velocity > vmax:
					velocity = vmax
				elif velocity < 0:
					velocity = 0
				
				# Create the new car
				car = Car(position,velocity,vmax,p,self.__lane_bit_state)
				self.__cars.append(car)
				
				# Make this car the head car if there isn't one already
				if head_car is None:
					head_car = car
					
				# Set the previous car's next_car to the current car
				if previous_car is not None: 
					previous_car.set_next_car(car)
					
				# Set previous_car to the current car for the next loop runthrough
				previous_car = car
			
			# Increment the iterator
			position += 1
		
		# Now that we're out of the loop, set the last car's next_car reference to
		# the head car
		previous_car.set_next_car(head_car)
		
		self.__car_count = len(self.__cars)
	
	## Private methods ##
	def __calc_new_velocities(self):
		for car in self.__cars:
			car.calc_new_velocity()
	
	def __move_cars(self):
		for car in self.__cars:
			looped = car.move()
			if looped:
				self.__loop_last_car()
	
	def __loop_last_car(self):
		self.__cars.insert(0,self.__cars.pop())
		
	## Public methods ##
	def step(self):
		self.__calc_new_velocities()
		self.__move_cars()
		self.__step_count += 1
		return self.get_lane_bit_state()
	
	def get_lane_bit_state(self):
		return list(self.__lane_bit_state)
	
	def get_lane_velocity_state(self):
 		lcl = [] # Lane condition list is empty to start
		ci = 0   # Specify this so that below we start by pulling the zeroth car from the car list (the first car)
		for bit_state in self.__lane_bit_state:
			if bit_state == True:
				lcl.append(self.__cars[ci].get_velocity()) # If true, we add the cars velocity to the list
				ci += 1 # Add so that next time it selects the next car in the list of cars
			else:
				lcl.append(None) # If false, we add None
				
	def get_lane_density(self):
		return float(len(self.__cars)) / len(self.__lane_bit_state)
	
	def get_average_velocity(self):
		vel_sum = 0
		for c in self.__cars:
			vel_sum += c.get_velocity()
		
		return float(vel_sum) / self.__car_count
	def get_slowing_probability(self):
		return self.__slowing_probability
	def get_max_velocity(self):
		return self.__max_velocity