#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 15:27:37 2018

@author: Morten
"""
from Vector import *
from Color import *

class Turtle:
    """This is the base class for all turtles."""

    def __init__(self, position, heading,
                       outline=black, fill=white, width=1):
        self.position, self.heading = position, heading
        self.style = dict(outline=outline, fill=fill, width=width)

    def getshape(self):
        """Return a list of vectors giving the polygon for this turtle."""
        forward = unit(self.heading)
        right = unit(self.heading + 90)
        return [self.position + forward*15,
                self.position - forward*8 - right*8,
                self.position - forward*5,
                self.position - forward*8 + right*8]

    def getnextstate(self):
        """Determine the turtle's next step and return its new state."""
        return self.position, self.heading

    def setstate(self, state):
        """Update the state of the turtle."""
        self.position, self.heading = state