from Tkinter import *
from functools import partial

class LaneControl:
	def __init__(self):
		print "Initalize LaneControl window"
		self.__root = Tk()
		
		# Set the parameters for the first time
		self.__reset_parameters()
		
		# Build the interface
		self.__build_parameter_frame()
		self.__populate_parameter_frame()
		
		print "Starting mainloop..."
		self.__root.mainloop()
		
	def __build_parameter_frame(self):
		self.__parameter_frame = LabelFrame(self.__root,text="Simulation Parameters")
		self.__parameter_frame.pack(side=LEFT)
	
	def __populate_parameter_frame(self):
		# Lane Size
		l = Label(self.__parameter_frame,text = "Lane Size")
		l.grid(row=0,column=0,sticky=W)
		self.__build_editable_input(
			self.__parameter_frame,
			self.__input_lane_size,
			self.__validate_lane_size
		).grid(row=0,column=1)
		
		# Max Velocity
		l = Label(self.__parameter_frame,text = "Max Velocity")
		l.grid(row=1,column=0,sticky=W)
		self.__build_editable_input(
			self.__parameter_frame,
			self.__input_max_velocity,
			self.__validate_max_velocity
		).grid(row=1,column=1)
	
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
			width=1,height=1,relief=FLAT,
			command=partial(self.__increment_textvariable,tv,1)
		).grid(row=0,column=1)
		
		# Down button
		Button(f,
			text=u"\u25BC",font=("Arial",7),
			width=1,height=1,relief=FLAT,
			command=partial(self.__increment_textvariable,tv,-1)
		).grid(row=1,column=1)
		
		return f
		
	def __increment_textvariable(self,textvariable,ammount):
		try:
			textvariable.set(int(textvariable.get()) + ammount)
		except:
			textvariable.set(0)

	def __reset_parameters(self):
		self.__input_lane_size = StringVar(value=10)
		self.__input_max_velocity = StringVar(value=1)
		
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

LaneControl()