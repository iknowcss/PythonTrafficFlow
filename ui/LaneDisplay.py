from Tkinter import *

class LaneDisplay:
	def __init__(self,lane):
		self.__root = Tk()
		print "- LaneDisplay initalized"
		print "- initial bit state: "
		print " ",lane.get_lane_bit_state()
		print "- initial velocity state: "
		print " ",lane.get_lane_velocity_state()
