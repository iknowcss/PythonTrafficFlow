from Tkinter import *
import time
import math
import operator
from threading import Thread

class LaneControl:
	default_car_size = 50
	max_canvas_size = 1000
	car_color_start = (250,70,70) #FA4646
	car_color_end = (66,168,102) #42A866
	car_color_head = (0,0,255) #0000FF
	canvas_color = "#ffffff"
	round_level = 3
	round_f = "%."+str(round_level)+"f"
	default_sleep_time = 0.1
	def __init__(self,lane_loader_ref,parameters):
		print
		print "Initalizing LaneControl Toplevel"
		self.__top = Toplevel()
		self.__top.protocol("WM_DELETE_WINDOW", self.__close_window_callback)
		
		print "Initalizing LaneControl variables"
		self.__original_parameters = parameters
		self.__lane_loader_ref = lane_loader_ref
		self.__lane = self.__build_lane_object(parameters)
		lbs = self.__lane.get_lane_bit_state()
		
		self.__lane_size = len(lbs)
		self.__car_count = sum(map(int,lbs))
		self.__blank_rectangles = None
		self.__car_rectangles = None
		self.__car_size = LaneControl.default_car_size
		self.__animation_canvas = None
		self.__animation_playing = False
		self.__play_pause_button = None
		self.__playing_disable_buttons = []
		self.__lane_density = self.__lane.get_lane_density()
		self.__lane_density_label = None
		self.__lane_avg_vel_label = None
		self.__lane_current_label = None
		self.__step_sleep_time = LaneControl.default_sleep_time
		
		print "Disabling LaneLoader"
		self.__lane_loader_ref.disable_controls()
		
		print "Preparing animation canvas"
		self.__build_animation_canvas()
		
		print "Preparing status frame"
		self.__build_status_frame()
	
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
		if canvas_width > LaneControl.max_canvas_size:
			ratio = float(LaneControl.max_canvas_size) / canvas_width
			ratio = math.floor(self.__car_size * ratio) / float(self.__car_size)
			self.__car_size = int(ratio * self.__car_size)
			canvas_width = self.__car_size * self.__lane_size + 2
		canvas_height = self.__car_size * 2
			
		
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
		
		# Speed
		speed = StringVar()
		speeds = ["1 ticks/sec","5 ticks/sec","10 ticks/sec","100 ticks/sec"]
		speed.set(speeds[-2])
		b = OptionMenu(pcframe,speed,*speeds,command=self.__set_animation_speed)
		b.config(width=15,justify=RIGHT)
		b.pack(side=LEFT)
		self.__playing_disable_buttons.append(b)
		
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
		lf.pack(fill=X,ipady=5)
	def __rewind_animation(self):
		self.__lane = self.__build_lane_object(self.__original_parameters)
		self.__color_offset = 0
		self.__first_car_pos = self.__lane.get_lane_bit_state().index(True)
		self.__trip_steps = 0
		self.__draw_bit_state()
		self.__update_simulation_status(True)
	def __set_animation_speed(self,speed_text):
		tps = int(speed_text[0:speed_text.index(" ")])
		self.__step_sleep_time = 1.0 / tps
		print self.__step_sleep_time
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
			time.sleep(self.__step_sleep_time)
	def __pause_animation(self):
		self.__animation_playing = False
		self.__play_pause_button.config(text=u"\u25BA",command=self.__play_animation)
		for b in self.__playing_disable_buttons:
			b.config(state=NORMAL)
	def __step_animation(self):
		self.__draw_bit_state(self.__lane.step())
		self.__update_simulation_status()
	def __draw_bit_state(self,lbs=None):
		# Get the lane bit state
		if lbs is None:
			lbs = self.__lane.get_lane_bit_state()
		
		# Do we need to re-add the rectangles?
		if self.__blank_rectangles is None or self.__car_rectangles is None:
			self.__blank_rectangles = []
			self.__car_rectangles = []
			self.__color_offset = 0
			self.__first_car_pos = lbs.index(True)
			self.__trip_steps = 0
			
			icolor = (
				LaneControl.car_color_start[0],
				LaneControl.car_color_start[1],
				LaneControl.car_color_start[2]
			)
			dcolor = list(LaneControl.car_color_end)
			for i in range(3):
				dcolor[i] -= LaneControl.car_color_start[i]
				dcolor[i] /= float(self.__car_count)
				dcolor[i] = int(math.floor(dcolor[i]))
			dcolor = tuple(dcolor)
			
			created_head = False
			for i in range(self.__lane_size):
				state = lbs[i]
				color = None
				if state is True:
					color = "#%02x%02x%02x" % icolor
					icolor = tuple(map(operator.add,icolor,dcolor))
					if created_head is False:
						print "Create Head rectangle"
						color = "#%02x%02x%02x" % LaneControl.car_color_head
						self.__car_peg = self.__animation_canvas.create_oval(
							0, self.__car_size,
							self.__car_size, 2 * self.__car_size,
							fill="#000000"
						)
						created_head = True
				else:
					color = LaneControl.canvas_color
				
				r = self.__animation_canvas.create_rectangle(
					0, 1,
					self.__car_size, self.__car_size,
					fill=color
				)
				if state is True:
					self.__car_rectangles.append(r)
				else:
					self.__blank_rectangles.append(r)
		
		looped = False
		if self.__first_car_pos - lbs.index(True) > 0:
			self.__color_offset = (self.__color_offset + 1) % self.__car_count
			looped = True
			
		if looped and self.__color_offset is 0:
			self.__last_trip_label.config(text=str(self.__trip_steps) + " steps")
			self.__trip_steps = 0
		else:
			self.__trip_steps += 1
			
		bri = 0
		cri = 0
		cra = range(-self.__color_offset,len(self.__car_rectangles)-self.__color_offset)
		for i in range(self.__lane_size):
			is_car_peg = False
			state = lbs[i]
			r = None
			if state is True:
				if cra[cri] is 0:
					is_car_peg = True
				r = self.__car_rectangles[cra[cri]]
				cri += 1
			else:
				r = self.__blank_rectangles[bri]
				bri += 1
				
			x = self.__car_size * i
			xoffset = [0,1][i==0]
			self.__animation_canvas.coords(r,
				x + 3, 1 + 3,
				x + self.__car_size + 3, self.__car_size + 3
			)
			
			if is_car_peg is True:
				self.__animation_canvas.coords(self.__car_peg,
					x + 3 + 1, self.__car_size + 3 + 2,
					x + self.__car_size + 3 - 1, 2 * self.__car_size + 3
				)
		self.__first_car_pos = lbs.index(True)
	def __update_simulation_status(self,empty=False):
		if empty:
			self.__lane_density_label.config(text=
				(LaneControl.round_f % round(self.__lane_density,LaneControl.round_level)) +
				" cars/space"
			)
			self.__slowing_prob_label.config(text=
				"%3.1f%%" % (self.__lane.get_slowing_probability() * 100)
			)
			self.__max_vel_label.config(text=self.__lane.get_max_velocity())
			self.__lane_avg_vel_label.config(text="[unknown]")
			self.__lane_current_label.config(text="[unknown]")
			self.__last_trip_label.config(text="[unknown]")
		else:
			vel = self.__lane.get_average_velocity()
			current = vel * self.__lane_density
			self.__lane_avg_vel_label.config(text=
				(LaneControl.round_f % round(vel,LaneControl.round_level)) + 
				" spaces/tick"
			)
			self.__lane_current_label.config(text=
				(LaneControl.round_f % round(current,LaneControl.round_level)) +
				" cars/tick"
			)
	def __build_status_frame(self):
		# Frame
		lf = LabelFrame(
			self.__top,
			text="Status"
		)
		
		# Lane Density
		Label(lf,text="Lane Density:").grid(row=0,column=0,padx=10,sticky=W)
		self.__lane_density_label = Label(lf)
		self.__lane_density_label.grid(row=0,column=1,padx=10,sticky=W)
		
		# Slowing Prob
		Label(lf,text="Slowing Prob:").grid(row=1,column=0,padx=10,sticky=W)
		self.__slowing_prob_label = Label(lf)
		self.__slowing_prob_label.grid(row=1,column=1,padx=10,sticky=W)
		
		# Max Velocity
		Label(lf,text="Max Velocity:").grid(row=2,column=0,padx=10,sticky=W)
		self.__max_vel_label = Label(lf)
		self.__max_vel_label.grid(row=2,column=1,padx=10,sticky=W)
		
		# Average Velocity
		Label(lf,text="Average Velocity:").grid(row=3,column=0,padx=10,sticky=W)
		self.__lane_avg_vel_label = Label(lf)
		self.__lane_avg_vel_label.grid(row=3,column=1,padx=10,sticky=W)
		
		# Current
		Label(lf,text="Current:").grid(row=4,column=0,padx=10,sticky=W)
		self.__lane_current_label = Label(lf)
		self.__lane_current_label.grid(row=4,column=1,padx=10,sticky=W)
		
		# Last trip
		Label(lf,text="Last trip:").grid(row=5,column=0,padx=10,sticky=W)
		self.__last_trip_label = Label(lf)
		self.__last_trip_label.grid(row=5,column=1,padx=10,sticky=W)
		
		lf.pack(fill=X,pady=5,ipadx=10)
		
		self.__update_simulation_status(True)
	
	def __close_window_callback(self):
		self.__pause_animation()
		self.__top.destroy()
		self.__lane_loader_ref.enable_controls()
