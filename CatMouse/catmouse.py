#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 15:44:25 2018

@author: Morten
"""

from tkinter import *                  # Import everything from Tkinter
from Arena   import Arena              # Import our Arena
from Turtle  import Turtle             # Import our Turtle
from Vector  import *                  # Import everything from our Vector
from Statue import Statue 
from Mouse import Mouse
from Cat import Cat
from globalVariables import *


statueRadius = 1
statuePosition = Vector(200,200)
mouseAngle = -57.0
catAngle = 0.0
catRadius = 4.0



tk = Tk()                                 # Create a Tk top-level widget
arena = Arena(tk)                         # Create an Arena widget, arena
arena.pack()                              # Tell arena to pack itself on screen
s = Statue(statuePosition, statueRadius)  # Add a turtle at (200,200) heading 0=up
m = Mouse(statue = s, angle = mouseAngle, arena = arena)
c = Cat(arena = arena, mouse = m, angle = catAngle, radius = catRadius)
arena.add(s)
arena.add(m)
arena.add(c)
tk.mainloop()         