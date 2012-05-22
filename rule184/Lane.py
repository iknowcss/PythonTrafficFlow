class Lane:
	# Constructor
	def __init__(self,initial_velocity_state):
		# Ensure the lane has more than one space
		self.__lane_length = len(initial_velocity_state)
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
	
	# Public methods
	def step(self):
		old = list(self.__lane_bit_state)
		for i in range(self.__lane_length):
			p = int(old[i - 1])
			q = int(old[i])
			r = int(old[(i + 1) % self.__lane_length])
			self.__lane_bit_state[i] = bool((p + p * q + q * r) % 2) # Rule 184
			#self.__lane_bit_state[i] = bool((p + q + r + q*r) % 2) # Rule 30
		return self.get_lane_bit_state()
	
	def get_lane_bit_state(self):
		return list(self.__lane_bit_state)
