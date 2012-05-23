import numpy as np
import random
import sys
class Car(object):
    ### Constructor ###
    def __init__(self,position,velocity,vmax,p,lane_bit_state_ref):
        """initializes"""
        self.__position = position
        self.__velocity = velocity
        self.__vmax = vmax
        self.__p = p
        self.__lane_bit_state_ref = lane_bit_state_ref
        self.__next_car_ref = None
        self.__g = 0
        
        
    def print_attributes(self):
        """prints attribultes in object"""
        for attr in self.__dict__:
            print attr,':',getattr(self,attr)
     
    ### Private Methods ###        
            
    def __do_slow_randomly(self):
        """chance of random slowing"""
        r = random.random()
        if r < self.__p:
            return True
        else:
            return False
            
    def __calc_new_g(self):
        """calculates new distance between obejct and next object"""
        if self.__next_car_ref.__position < self.__position:
            self.__g = self.__next_car_ref.__positon + len(lane_bit_state_ref) - self.__position - 1
        else:
            self.__g = self.__next_car_ref.__position - self.__position - 1
    
        
    ### Public Methods ###    
        
    def get_velocity(self):
        """returns velocity of object"""
        return self.__velocity
    
    def get_position(self):
        """returns position of object"""
        return self.__position
    
    def get_next_car(self):
        """returns position of next object"""
        return self.__next_car_ref
    
    def set_next_car(self,other):           
        """sets the next object to other"""
        self.__next_car_ref = other
        
    def calc_new_velocity(self):
        """calculates new velocity"""
        self.__calc_new_g()
        if self.__velocity > self.__g:
            self.__velocity = self.__g
        elif self.__velocity < self.__g and self.__velocity < self.__vmax:
            self.__velocity += 1
        if self.__velocity > 0:
            if self.__do_slow_randomly == True:
                self.__velocity -= 1
            
    def move(self):
        """moves object in lane, returns True if car loops back to start of lane, returns False otherwise"""
        self.__position = self.get_position() + self.get_velocity()
        if self.__position > len(lane_bit_state_ref):
            self.__position = self.__position % len(lane_bit_state_ref)
            return True
        else:
            return False