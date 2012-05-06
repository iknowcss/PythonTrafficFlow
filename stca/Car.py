import numpy
class Car:
	# Constructor
	def __init__(self,position,velocity,vmax,p,lane_bit_state_ref):
		self.__position = position
		self.__velocity = velocity
		self.__vmax = vmax
		self.__p = p
		self.__lane_bit_state_ref = lane_bit_state_ref
		
	# Private methods
	def __do_slow_randomly(self):
		print "TODO: implement Car#__do_slow_randomly()"
		
	def __calc_new_g(self):
		print "TODO: implement Car#__calc_new_g()"
	
	# Public methods
	def get_velocity(self):
		print "TODO: implement Car#get_velocity()"
		
	def get_position(self):
		r = numpy.random.random() # a random value "r" where 0.0 <= r < 1.0
		print "TODO: implement Car#get_position()"
		
	def get_next_car(self):
		print "TODO: implement Car#get_next_car()"
		
	def set_next_car(self,car):
		print "TODO: implement Car#set_next_car(car)"
		
	def calc_new_velocity(self):
		print "TODO: implement Car#calc_new_velocity()"
		
	def move(self):
		print "TODO: implement Car#move()"
