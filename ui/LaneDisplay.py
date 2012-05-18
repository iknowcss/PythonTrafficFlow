from Tkinter import *
from functools import partial

class LaneDisplay:
	scale = 10
	car_color = "#42A866"
	canvas_color = "#ffffff"
	def __init__(self,lane,steps=50):
		# Begin initalization
		print "- Initializing LaneDisplay"
		
		# Check the bit state
		lane_bit_state = lane.get_lane_bit_state()
		print "- initial bit state: "
		print " ",lane_bit_state
		self.__lane_length = len(lane_bit_state)
		self.__steps = steps
		
		# Check the velocity state (if possible)
		if hasattr(lane,"get_lane_velocity_state"):
			print "- initial velocity state: "
			print " ",lane.get_lane_velocity_state()
		
		# Get a reference to the lane
		self.__lane = lane
		
		# Initalize tkinter
		self.__init_tkinter()

	def __init_tkinter(self):
		# Prepare the root
		self.__root = Tk()
		
		# Construct, add, and prepare the Canvas
		self.__canvas = Canvas(self.__root,\
			width=LaneDisplay.scale * self.__lane_length,\
			height=LaneDisplay.scale * self.__steps,\
			bd=0\
		)
		self.__canvas.pack(side=LEFT)
		self.__ready_canvas()
		
		# Function to run when mainloop begins
		self.__root.after(0,partial(self.run,self.__steps))
		
		# Start the mainloop
		self.__root.mainloop()
	
	def __ready_canvas(self):
		self.__canvas.create_rectangle(\
			0,0,\
			self.__lane_length * LaneDisplay.scale,self.__steps * LaneDisplay.scale,\
			fill=LaneDisplay.canvas_color,\
			width=0\
		)
	
	def draw_car(self,sx,sy):
		self.__canvas.create_rectangle(\
			sx * LaneDisplay.scale,sy * LaneDisplay.scale,\
			(sx + 1) * LaneDisplay.scale,(sy + 1) * LaneDisplay.scale,\
			fill=LaneDisplay.car_color,\
			width=0\
		)
		
	def draw_lane_bit_state(self,lane_bit_state=None,y_offset=0):
		if lane_bit_state is None:
			lane_bit_state = self.__lane.get_lane_bit_state()
		for j in range(self.__lane_length):
			if lane_bit_state[j]:
				self.draw_car(j,y_offset)
	
	def step(self):
		return self.__lane.step()
		
	def run(self,steps=10):
		for i in range(steps):
			if i == 0:
				self.draw_lane_bit_state()
			else:
				self.draw_lane_bit_state(self.step(),i)
