import os
import json
from Tkinter import *
from LaneControl import LaneControl

class LaneLoader:
	def __init__(self,sim_type_dict={}):
		print
		print "Initalizing LaneLoader window"
		self.__root = Tk()
		
		print "Initalizing LaneLoader variables"
		self.__main_frame = None
		self.__file_select_dropdown = None
		self.__run_simulation_button = None
		self.__selected_file_name = StringVar()
		self.__file_paths = {}
		self.__sim_type_dict = sim_type_dict
		
		print "Loading file names"
		self.__load_demo_file_names()
		
		print "Preparing main frame"
		self.__prepare_main_frame()
		
		print "Starting mainloop..."
		self.__root.mainloop()
	
	def __load_demo_file_names(self):
		for dirname, dirnames, filenames in os.walk("demos"):
			for filename in filenames:
				ext = filename.split(".").pop().lower()
				file_path = ""
				if ext == "json":
					file_path = os.path.join(dirname, filename)
				else:
					continue
				
				self.__file_paths[filename] = file_path
	def __prepare_main_frame(self):
		self.__main_frame = LabelFrame(
			self.__root,
			text="Load Traffic Flow File"
		)
		self.__main_frame.pack(fill=BOTH,ipadx=3)
		
		print "Preparing file select dropdown"
		self.__prepare_file_select_dropdown()
		
		self.__run_simulation_button = Button(
			self.__main_frame,
			text="Run",
			command=self.__run_simulation_button_click
		)
		self.__run_simulation_button.grid(row=0,column=1,padx=2,pady=5)
	def __prepare_file_select_dropdown(self):
		options = self.__file_paths.keys()
		options.sort()
		max_length = 0
		for o in options:
			l = len(o)
			if l > max_length:
				max_length = l
		self.__file_select_dropdown = OptionMenu(
			self.__main_frame,
			self.__selected_file_name,
			*options
		)
		self.__file_select_dropdown.config(width=max_length,anchor=W)
		self.__file_select_dropdown.grid(row=0,column=0,padx=2,pady=5)
		if len(options) > 0:
			self.__selected_file_name.set(options[0])
	def __set_main_frame_state(self,state):
		for c in [self.__file_select_dropdown,self.__run_simulation_button]:
			if c is None:
				continue
			c.config(state=state)
	def __run_simulation_button_click(self):
		file_path = self.__file_paths[self.__selected_file_name.get()]
		self.__run_file(file_path)
	def __run_file(self,file_path):
		print "Preparing to parse file \"" + file_path + "\""
		parameters = None
		try:
			json_dict = self.__parse_file(file_path)
			if type(json_dict) is not dict:
				raise TypeError("self.__parse_file() did not return a dict")
			parameters = LaneParameters(self.__sim_type_dict,json_dict)
		except Exception as e:
			print "There was a problem parsing the file:",e
			return
		
		# File was loaded successfully
		print "Preparing LaneControl"
		LaneControl(self,parameters)
	def __parse_file(self,file_path):
		try:
			print "Parsing file"
			json_data = open(file_path)
			return json.load(json_data)
		finally:
			print "Closing file"
			json_data.close()
		
	def disable_controls(self):
		self.__set_main_frame_state(DISABLED)
	def enable_controls(self):
		self.__set_main_frame_state(NORMAL)
		
class LaneParameters:
	def __init__(self,sim_type_dict,json_dict):
		self.initial_conditions = list(json_dict[u"initialConditions"])
		self.max_velocity = int(json_dict[u"maxVelocity"])
		self.slowing_probability = float(json_dict[u"slowingProbability"])
		self.is_simple_ca = False
		
		simulation_class = None
		simulation_type_name = json_dict[u"simulationType"].lower()
		try:
			simulation_class = sim_type_dict[simulation_type_name]
			if simulation_class is None:
				raise
			if simulation_type_name == "rule184":
				self.is_simple_ca = True
		except Exception:
			raise Exception("Could not load simulation type \"" + simulation_type_name + "\"")
		
		self.simulation_class = simulation_class
        
	def print_attributes(self,prefix=""):
		for attr in self.__dict__:
			print prefix + attr,':',getattr(self,attr)