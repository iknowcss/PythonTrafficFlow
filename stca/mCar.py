import numpy as np
import random
class Car(object):
    def __init__(self,position,velocity,vmax,p,lane_bit_state_ref):
        """initializes"""
        self.position = position
        self.velocity = velocity
        self.vmax = vmax
        self.p = p
        self.lane_bit_state_ref = lane_bit_state_ref
        self.next_car_ref = None
        self.g = 0
        
        
    def print_attributes(self):
        """prints attribultes in object"""
        for attr in self.__dict__:
            print attr,':',getattr(self,attr)
            
    def do_slow_randomly(self):
        """chance of random slowing"""
        r = random.random()*100
        if r <= p:
            self.velocity -= 1
            
    def calc_new_g(self):
        """calculates new distance between obejct and next object"""
        if self.next_car_ref is not None:
            self.g = self.next_car_ref.position - self.position - 1
        else:
            self.g = len(lane_bit_state_ref) - self.position - 1
        
    def get_velocity(self):
        """returns velocity of object"""
        return self.velocity
    
    def get_position(self):
        """returns position of object"""
        return self.position
    
    def get_next_car(self):
        """returns position of next object"""
        return self.next_car_ref
    
    def set_next_car(self,other):           
        """sets the next object to other"""
        self.next_car_ref = other
        
    def calc_new_velocity(self):
        """calculates new velocity"""
        if self.velocity > self.g:
            self.velocity = self.g
        elif self.velocity < self.g and self.velocity < self.vmax:
            self.velocity += 1
        if self.velocity > 0:
            self.do_slow_randomly
            
        
    def move(self):
        """moves object in lane"""
        self.position = self.position + self.velocity