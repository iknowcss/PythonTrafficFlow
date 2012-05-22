from Tkinter import *
import time
import math
from threading import Thread

class LaneControl:
	default_car_size = 50
	max_canvas_size = 800
	car_color = "#42A866"
	canvas_color = "#ffffff"
	def __init__(self,lane_loader_ref,parameters):
		print
		print "Initalizing LaneControl Toplevel"
		self.__top = Toplevel()
		self.__top.protocol("WM_DELETE_WINDOW", self.__close_window_callback)
		
		print "Initalizing LaneControl variables"
		self.__original_parameters = parameters
		self.__lane_loader_ref = lane_loader_ref
		self.__lane = self.__build_lane_object(parameters)
		self.__lane_size = len(self.__lane.get_lane_bit_state())
		self.__blank_rectangles = None
		self.__car_rectangles = None
		self.__car_size = LaneControl.default_car_size
		self.__animation_canvas = None
		self.__animation_playing = False
		self.__play_pause_button = None
		self.__playing_disable_buttons = []
		
		print "Disabling LaneLoader"
		self.__lane_loader_ref.disable_controls()
		
		print "Preparing animation canvas"
		self.__build_animation_canvas()
	
	def __build_lane_object(self,parameters):
		print "Building lane with the following parameters:"
		
		if parameters.is_simple_ca:
			if hasattr(parameters,"max_velocity"):
				del parameters.max_velocity
			if hasattr(parameters,"slowing_probability"):
				del parameters.slowing_probability
			parameters.print_attributes(" - ")
			return parameters.simulation_class(
				parameters.initial_conditions
			)
		else:
			parameters.print_attributes(" - ")
			return parameters.simulation_class(
				parameters.max_velocity,
				parameters.slowing_probability,
				parameters.initial_conditions
			)
	def __build_animation_canvas(self):
		# Frame
		lf = LabelFrame(
			self.__top,
			text="Simulation"
		)
		
		# Canvas
		canvas_width = self.__car_size * self.__lane_size
		canvas_height = self.__car_size
		
		# Ensure Canvas dimensions
		if canvas_width > LaneControl.max_canvas_size:
			ratio = float(LaneControl.max_canvas_size) / canvas_width
			ratio = math.floor(self.__car_size * ratio) / float(self.__car_size)
			self.__car_size = int(ratio * self.__car_size)
			canvas_width = self.__car_size * self.__lane_size
			canvas_height = self.__car_size
			
		
		self.__animation_canvas = Canvas(
			lf,
			width=canvas_width,
			height=canvas_height + 1
		)
		self.__animation_canvas.pack(fill=BOTH,padx=5,pady=5)
		
		# Cars
		self.__draw_bit_state()
		
		# Player controls
		pcframe = Frame(lf)
		
		# Rewind
		b = Button(pcframe,text=u"\u21BA",font="Courier",command=self.__rewind_animation)
		b.pack(side=LEFT)
		self.__playing_disable_buttons.append(b)
		
		# Play/Pause
		b = Button(pcframe,font="Courier")
		b.pack(side=LEFT)
		self.__play_pause_button = b
		
		# Step
		b = Button(pcframe,text=u"\u003E",font="Courier",command=self.__step_animation)
		b.pack(side=LEFT)
		self.__playing_disable_buttons.append(b)
		
		pcframe.pack()
		self.__pause_animation()
		
		# Final pack
		lf.pack(ipady=5)
	def __rewind_animation(self):
		self.__lane = self.__build_lane_object(self.__original_parameters)
		self.__draw_bit_state()
	def __play_animation(self):
		self.__animation_playing = True
		self.__play_pause_button.config(text=u"\u25A3",command=self.__pause_animation)
		for b in self.__playing_disable_buttons:
			b.config(state=DISABLED)
		Thread(target=self.__play_animation_thread).start()
	def __play_animation_thread(self):
		while True:
			if not self.__animation_playing:
				break
			self.__step_animation()
			time.sleep(0.1)
	def __pause_animation(self):
		self.__animation_playing = False
		self.__play_pause_button.config(text=u"\u25BA",command=self.__play_animation)
		for b in self.__playing_disable_buttons:
			b.config(state=NORMAL)
	def __step_animation(self):
		self.__draw_bit_state(self.__lane.step())
	def __draw_bit_state(self,lbs=None):
		# Get the lane bit state
		if lbs is None:
			lbs = self.__lane.get_lane_bit_state()
		
		# Do we need to re-add the rectangles?
		if self.__blank_rectangles is None or self.__car_rectangles is None:
			self.__blank_rectangles = []
			self.__car_rectangles = []
			for i in range(self.__lane_size):
				state = lbs[i]
				color = [LaneControl.canvas_color,LaneControl.car_color][state]
				r = self.__animation_canvas.create_rectangle(
					0, 1,
					self.__car_size, self.__car_size,
					fill=color
				)
				if state is True:
					self.__car_rectangles.append(r)
				else:
					self.__blank_rectangles.append(r)
		
		bri = 0
		cri = 0
		for i in range(self.__lane_size):
			state = lbs[i]
			r = None
			if state is True:
				r = self.__car_rectangles[cri]
				cri += 1
			else:
				r = self.__blank_rectangles[bri]
				bri += 1
				
			x = self.__car_size * i
			xoffset = [0,1][i==0]
			self.__animation_canvas.coords(r,
					x, 1,
					x + self.__car_size, self.__car_size
			)
			
	def __close_window_callback(self):
		self.__top.destroy()
		self.__lane_loader_ref.enable_controls()