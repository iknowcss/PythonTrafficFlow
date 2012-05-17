from Tkinter import *
from functools import partial

class LaneControl:
	ic_row_count = 10

	# Initalization
	def __init__(self):
		print "Initalize LaneControl window"
		self.__root = Tk()
		
		# Set the parameters for the first time
		self.__reset_parameters()
		
		# Build the interface
		self.__build_parameter_frame()
		self.__build_ic_frame()
		
		print "Starting mainloop..."
		self.__root.mainloop()
	
	# Simulation Parameter Functions
	def __build_parameter_frame(self):
		self.__parameter_frame = LabelFrame(self.__root,
			text="Simulation Parameters"
		)
		self.__parameter_frame.pack(fill=BOTH,padx=10,pady=5)
		self.__populate_parameter_frame()
	def __populate_parameter_frame(self):
		self.__parameter_inputs = []
	
		# Lane Size
		l = Label(self.__parameter_frame,text = "Lane Size",padx=10)
		l.grid(row=0,column=0,sticky=W)
		ei = self.__build_editable_input(
			self.__parameter_frame,
			self.__input_lane_size,
			self.__validate_lane_size
		)
		ei.grid(row=0,column=1)
		self.__parameter_inputs.append(ei)
		
		# Max Velocity
		l = Label(self.__parameter_frame,text = "Max Velocity",padx=10)
		l.grid(row=1,column=0,sticky=W)
		ei = self.__build_editable_input(
			self.__parameter_frame,
			self.__input_max_velocity,
			self.__validate_max_velocity
		)
		ei.grid(row=1,column=1)
		self.__parameter_inputs.append(ei)
		
		# Slowing Probability
		l = Label(self.__parameter_frame,text="Slowing Probability\n(percentage)",padx=10,justify=LEFT)
		l.grid(row=0,column=2,sticky=W)
		ei = self.__build_editable_input(
			self.__parameter_frame,
			self.__input_slowing_prob,
			self.__validate_slowing_prob
		)
		ei.grid(row=0,column=3)
		self.__parameter_inputs.append(ei)
		
		# Apply Parameters
		self.__button_apply_parameters = Button(self.__parameter_frame,
			text="Apply Parameters",
			command=self.__apply_parameters,
			width=15
		)
		self.__button_apply_parameters.grid(row=1,column=2,columnspan=2)
	def __apply_parameters(self):
		self.__button_apply_parameters.configure(
			text="Edit Parameters",
			command=self.__edit_parameters
		)
		self.__disable_parameter_inputs()
	def __edit_parameters(self):
		self.__button_apply_parameters.configure(
			text="Apply Parameters",
			command=self.__apply_parameters
		)
		self.__enable_parameter_inputs()
	def __reset_parameters(self):
		self.__input_lane_size = StringVar(value=10)
		self.__input_max_velocity = StringVar(value=1)
		self.__input_slowing_prob = StringVar(value=0)
	def __enable_parameter_inputs(self):
		for pi in self.__parameter_inputs:
			for c in pi.winfo_children():
				c.config(state=NORMAL)
	def __disable_parameter_inputs(self):
		for pi in self.__parameter_inputs:
			for c in pi.winfo_children():
				c.config(state=DISABLED)
	
	# Initial Condition Functions
	def __build_ic_frame(self):
		self.__ic_frame = LabelFrame(self.__root,
			text="Initial Conditions"
		)
		self.__ic_frame.pack(fill=BOTH,padx=10,pady=5)
		self.__populate_ic_frame()
	def __populate_ic_frame(self):
		for j in range(3):
			f = Frame(self.__ic_frame)
			f.pack()
			for i in range(LaneControl.ic_row_count):
				Button(f,
					text=i + LaneControl.ic_row_count*j,
					font="Courier",
					bd=0,
					bg="#ff00ff",
					relief=FLAT,
					width=1
				).grid(row=j,column=i)
	
	# UI Util
	def __build_editable_input(self,parent,tv,handler,width=5,justify=RIGHT):
		# Prepare frame
		f = Frame(parent)
		e = Entry(f,textvariable=tv,width=width,justify=justify)
		e.grid(row=0,column=0,rowspan=2)
		
		# Ensure valid value
		tv.trace("w",lambda name,index,mode,tv=tv:handler(tv))
		
		# Up button
		Button(f,
			text=u"\u25B2",font=("Arial",7),
			width=2,height=1,relief=FLAT,bd=0,
			padx=0,pady=0,
			command=partial(self.__increment_textvariable,tv,1)
		).grid(row=0,column=1)
		
		# Down button
		Button(f,
			text=u"\u25BC",font=("Arial",7),
			width=2,height=1,relief=FLAT,bd=0,
			padx=0,pady=0,
			command=partial(self.__increment_textvariable,tv,-1)
		).grid(row=1,column=1)
		
		return f
	def __increment_textvariable(self,textvariable,ammount):
		try:
			textvariable.set(int(textvariable.get()) + ammount)
		except:
			textvariable.set(0)
	
	# Validation
	def __validate_int(self,sv,min,max):
		try:
			cur = sv.get()
			if len(cur) == 0:
				return
			cur = float(sv.get())
			if cur - int(cur) != 0:
				raise
			if cur < min:
				sv.set(min)
			elif cur > max:
				sv.set(max)
		except:
			sv.set(min)
	def __validate_lane_size(self,sv):
		self.__validate_int(sv,2,20)
	def __validate_max_velocity(self,sv):
		self.__validate_int(sv,1,1000)
	def __validate_slowing_prob(self,sv):
		self.__validate_int(sv,0,100)

LaneControl()
