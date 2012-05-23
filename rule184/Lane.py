class Lane:
	# Constructor
	def __init__(self,initial_velocity_state):
		# Ensure the lane has more than one space
		self.__lane_length = len(initial_velocity_state)
		self.__car_count = 0
		if self.__lane_length < 2:
			raise Exception("Degenerate initial conditions provided")
		
		# Initalize lists
		t = type(initial_velocity_state[0])
		if t is bool:
			self.__lane_bit_state = list(initial_velocity_state)
		else:
			self.__lane_bit_state = [False] * self.__lane_length
			for i in range(self.__lane_length):
				if initial_velocity_state[i] is not None:
					self.__lane_bit_state[i] = True
			
		self.__prev_lane_bit_state = list(self.__lane_bit_state)
		for bs in self.__lane_bit_state:
			if bs is True:
				self.__car_count += 1
	
	# Public methods
	def step(self):
		old = list(self.__lane_bit_state)
		for i in range(self.__lane_length):
			p = int(old[i - 1])
			q = int(old[i])
			r = int(old[(i + 1) % self.__lane_length])
			self.__lane_bit_state[i] = bool((p + p * q + q * r) % 2) # Rule 184
		self.__prev_lane_bit_state = old
		return self.get_lane_bit_state()
	
	def get_lane_bit_state(self):
		return list(self.__lane_bit_state)
		
	def get_lane_density(self):
		return float(self.__car_count) / self.__lane_length
	
	def get_average_velocity(self):
		vel_sum = 0
		for i in range(self.__lane_length):
			if not self.__prev_lane_bit_state[i] and self.__lane_bit_state[i]:
				vel_sum += 1
				
		return float(vel_sum) / self.__car_count
