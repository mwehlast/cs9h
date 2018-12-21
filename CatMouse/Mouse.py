#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:31:00 2018

@author: Morten
"""

from Turtle import *
from Color import *
from Vector import Vector
from globalVariables import *

import math

class Mouse(Turtle): #Inherit from Turtle Class Object
    
    def __init__(self, statue, arena, angle, outline=black, fill=yellow, width=1):
        
        self.statue = statue
        self.radius = statue.radius #Use same radius of statue as statue
        self.anchor = statue.position #Anchor position the mouse is running around
        self.angle = angle# % 360 #Starting angle for the mouse
        
        #Add mouse at the base of the statue
        self.position = self.anchor + unit(self.angle)*self.radius
        
        #Mouse should be perpendicular to angle provided (subtract to face counter-clockwise)
        self.heading = self.angle - 90 
         
        #Add original values
        self.origPos = self.position
        self.origAngle = self.angle
        self.origHeading = self.heading
        
        self.arena = arena #add arena object
        
        self.type = "Mouse" #Define type for updating label
        
        self.arena.mouseAngle.set('MouseAngle: {0:.1f}'.format(self.angle)) #Update initial label

        self.style = dict(outline=outline, fill=fill, width=width)
        
        
    
    def getnextstate(self):
        """Update position by moving mouse 1 meter per time step"""
        
        self.angle = (self.position - self.statue.position).direction()
        theta = -1/(self.radius*px2m)*rad2deg
        self.angleNew = (self.angle + theta / 100)# % 360 #Update according to length of arc formula
        self.position = self.anchor + unit(self.angleNew)*self.radius #Update to new position
        self.heading = self.angle - 90 #Update new heading
        return self.position, self.heading
        
        
    def reset(self):
        """Reset mouse to initial values"""
        
        self.angle = self.origAngle
        
        return self.origPos, self.origHeading
        
        
        
        