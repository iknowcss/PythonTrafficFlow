import numpy
class Car:
	# Constructor
	def __init__(self,position,velocity,vmax,p,lane_bit_state_ref):
		self.__vmax = vmax
		self.__p = p
		self.__g = 0
		self.__velocity = velocity
		self.__position = position
		self.__next_car_ref = None
		self.__lane_bit_state_ref = lane_bit_state_ref
		
	# Private methods
	def __do_slow_randomly(self):
		"""TODO: implement Car#__do_slow_randomly()"""
		
	def __calc_new_g(self):
		"""TODO: implement Car#__calc_new_g()"""

	# Public methods
	def get_velocity(self):
		"""TODO: implement Car#get_velocity()"""

	def get_position(self):
		"""TODO: implement Car#get_position()"""

	def get_next_car(self):
		"""TODO: implement Car#get_next_car()"""

	def set_next_car(self,car):
		"""#TODO: implement Car#set_next_car(car)"""

	def calc_new_velocity(self):
		"""#TODO: implement Car#calc_new_velocity()"""

	def move(self):
		"""#TODO: implement Car#move()"""
