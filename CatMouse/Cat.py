#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 13:00:31 2018

@author: Morten
"""

from Turtle import Turtle
from Vector import *
from Color import *
import math
from globalVariables import *

class Cat(Turtle): #Inherit from Turtle Class Object
    """A Cat Class Object tries to catch the mouse"""
    
    #Overwrite init
    def __init__(self, arena, mouse, angle, radius, outline=black, fill=blue, width=1):
        
        self.radius = radius*m2px #Use input value radius
        self.anchor = mouse.anchor #Anchor position the cat is running around
        self.angle = angle % 360 #Starting angle for the cat
        
        #Add cat at radius and angle given
        self.position = self.anchor + unit(self.angle)*self.radius
        
        #Cat should be perpendicular to angle provided (subtract to face counter-clockwise)
        self.heading = angle - 90 
        
        #Add mouse to access position
        self.mouse = mouse
        
        #Add arena
        self.arena = arena
        
        #Style cat
        self.style = dict(outline=outline, fill=fill, width=width)
        
        #Add original values
        self.origPos = self.position
        self.origAngle = self.angle
        self.origRadius = self.radius
        self.origHeading = self.heading
        
        #Update values in labels
        self.arena.catAngle.set('CatAngle: {0:.1f}'.format(self.angle))
        self.arena.catRadius.set('CatRadius: {0:.3f}'.format(self.radius*px2m))
        
        #Add original filling
        self.origFill = fill
        self.origOutline = outline
        
        self.type = "Cat" #Define type for updating labels
        
    def getnextstate(self):
        """Update state based on whether Cat has seen mouse or not """
        
        theta = -1.25/(self.radius*px2m)*rad2deg
        self.angleNew = (self.angle + theta / 100) % 360
        
        if self.arena.get_timestamp() >= self.arena.catBoredLevel * sec2ms: #Check if cat has gotten bored
            if self.arena.get_timestamp() == self.arena.catBoredLevel * sec2ms and printLogs: #Print to log
                self.printLogBored()
            
            
            self.radius = self.radius + 1*m2px/100 #Add one timestep to radius
            
            
            if self.angle <= 180: #Make sure cat runs to the right if right of statue
                self.position = self.anchor + unit(self.angle)*self.radius
                self.heading = self.angle
                return self.position, self.heading
            
            self.position = self.anchor + unit(self.angle)*self.radius #Cat runs left if left of statue
            self.heading = self.angle
            return self.position, self.heading

        
        
        if self.cancatchmouse(): #Check if mouse can be caught
            print("Tom ate Jerry at Timestep: {}".format(self.arena.get_timestamp() / 1000))
            if printLogs:
                self.printLogCatch() #Print to log
            self.arena.stop()
            
        if self.mouseseen():
            self.radius = self.radius - 1*m2px/100 #Move one meter closer per second
                
            if self.radius < self.mouse.radius: #Check Cat isnt jumping inside statue
                self.radius = self.mouse.radius
                
            #Update position accordingly
            self.position = self.anchor + unit(self.angle)*self.radius
            self.heading = self.angle + 180
                
        else: #In case mouse cannot be seen
            self.angle = self.angleNew
            self.position = self.anchor + unit(self.angle)*self.radius
            self.heading = self.angle - 90 #Perpendicular heading to angle
        
        if debug:
            self.debugPrint()
            
        return self.position, self.heading

    def mouseseen(self): #Method for evaluating if mouse is seen
        """Returns True if mouse can be seen from cat's position"""
        
        angleDifference = (self.angle - self.mouse.angle)
        
        return self.radius*px2m*cos(angleDifference*deg2rad) >= 1.0
        
    def cancatchmouse(self): #Method for evaluating if cat can catch mouse
        """Returns True if given conditions apply in order to catch mouse"""

        A = self.angle
        B = self.mouse.angle
        C = self.angleNew
        
        #Check conditions
        radiusIsOne = self.radius*px2m - 1 < 0.001
        mouseBetween = cos((B - A)*deg2rad) > cos((C - A)*deg2rad) and \
                        cos((C - B)*deg2rad) > cos((C - A)*deg2rad)
            
        return radiusIsOne and mouseBetween #Check all conditions apply
        
            
    def reset(self):
        """Resets cat back to initial values."""
        
        self.angle = self.origAngle
        self.radius = self.origRadius
        
        return self.origPos, self.origHeading
    
    def debugPrint(self):
        """Prints cat and mouse values to console for debugging purposes"""
        
        print("\nTimestamp: " + str(self.arena.get_timestamp() / 10))
        print("Cat Angle: {0:.4f}".format(self.angle))
        print("Cat Radius: {0:.4f}".format(self.radius*px2m))
        print("Mouse Angle: {0:.4f}".format(self.mouse.angle))
        
    def printLogCatch(self):
        """Prints test results to txt-file if mouse caught"""
        
        f = open('results.txt', 'a')
        f.write("-------------------\n")
        f.write("For values: \n")
        f.write("Cat Radius (m): {}\n".format(self.origRadius*px2m))
        f.write("Cat Angle: {}\n".format(self.origAngle))
        f.write("Mouse Angle: {}\n".format(self.mouse.origAngle))
        f.write("Tom ate Jerry at time: {} \n\n".format(self.arena.get_timestamp() / 1000))
        f.close()
    
    def printLogBored(self):
        """Prints test results to text-file if cat got bored"""     
        
        f = open('results.txt', 'a')
        f.write("-------------------\n")
        f.write("For values: \n")
        f.write("Cat Radius (m): {}\n".format(self.origRadius*px2m))
        f.write("Cat Angle: {}\n".format(self.origAngle))
        f.write("Mouse Angle: {}\n".format(self.mouse.origAngle))
        f.write("Tom got bored and left at time: {} (based on user scale input)\n\n".format(self.arena.get_timestamp() / 1000))
        f.close()