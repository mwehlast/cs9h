#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 15:37:49 2018

@author: Morten
"""

from Turtle import *
from Color import *
from Vector import Vector
from globalVariables import *


class Statue(Turtle): #Inherit from Turtle Class Object
    def __init__(self, position, radius, outline = black, fill = white, width = 1):
        
        self.position, self.heading, self.radius = position, 0, radius*m2px
        self.style = dict(outline=outline, fill=fill, width=width)
        
        self.type = "Statue" #Define type to update label
        
    def getshape(self):
        """
        Return a list of vectors giving the polygon for the statue
        Change numPoints to make outline more coarse/fine
        """
        
        numPoints = 100
        pointsArray = []
        forward = unit(self.heading)
        
        for i in range(numPoints):
            #Add rotated vector to current position and append
            pointsArray.append(self.position + forward.rotate(i*(360/numPoints))*self.radius)
        
        return pointsArray #Return all the new points.

    def reset(self):
        """Dummy reset method for the reset functionality in Arena"""
        return self.position, self.heading