#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 15:27:57 2018

@author: Morten
"""

from tkinter import *
from math import sin, cos, pi
from Vector import *
from Color import *
from globalVariables import *

class Arena(Frame):
    """This class provides the user interface for an arena of turtles."""

    def __init__(self, parent, width=400, height=400, **options):
        Frame.__init__(self, parent, **options)
        self.width, self.height = width, height
        self.canvas = Canvas(self, width=width, height=height)
        self.canvas.pack()
        
        #Add Menu
        parent.title("UC Berkeley CS9H Turtle Arena")
        menubar = Menu(parent)
        fileMenu = Menu(menubar, tearoff = 0)
        menubar.add_cascade(label = "File", menu = fileMenu)
        fileMenu.add_command(label = "About...", command = self.about)
        fileMenu.add_command(label = "Quit", command = parent.destroy)
        parent.config(menu = menubar)
        
        Button(self, text='step', command=self.step).pack(side=LEFT)
        Button(self, text='run', command=self.run).pack(side=LEFT)
        Button(self, text='stop', command=self.stop).pack(side=LEFT)
        Button(self, text='reset', command=self.reset).pack(side=LEFT)
        Button(self, text='quit', command=parent.quit).pack(side=LEFT)
        
        self.time = 0.0
        
        self.timeText = StringVar()
        self.timeText.set('Time: '+str(self.time))
        self.timeLabel = Label(self,textvariable=self.timeText)
        self.timeLabel.pack()
        
        self.catRadius = StringVar() #cat radius string
        self.catRadius.set('CatRadius: ')
        self.catRadiusLabel = Label(self, textvariable = self.catRadius)
        
        self.catAngle = StringVar() #cat angle string
        self.catAngle.set('CatAngle: ')
        self.catAngleLabel = Label(self, textvariable = self.catAngle)
        
        self.mouseAngle = StringVar() #mouse angle string
        self.mouseAngle.set('Mouse Angle: ')
        self.mouseAngleLabel = Label(self, textvariable = self.mouseAngle)
        
        self.catAngleLabel.pack()
        self.catRadiusLabel.pack()
        self.mouseAngleLabel.pack()
         
        
        #Add Scale (Own Widget)
        self.catBoredLevel = 30
        self.scale = Scale(parent, from_=0, \
                      to = 100, \
                      resolution=0.01, \
                      orient=HORIZONTAL, \
                      label = "Set Cat Boredness Level", \
                      width = 10, \
                      length = 170, \
                      command = self.set_boredlevel)
        self.scale.set(self.catBoredLevel) #Set scale to default value
        self.scale.pack()
        
        
        
        self.turtles = []
        self.items = {}
        self.running = 0
        self.period = 10 # milliseconds
        self.canvas.bind('<ButtonPress>', self.press)
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<ButtonRelease>', self.release)
        self.dragging = None

    #Add Scale Widget method
    def set_boredlevel(self, var):
        self.catBoredLevel = float(var)
    
    
    #Add "About"
    def about(self):
        """The about section holds information about the author and the program """
        about = Toplevel(self)
        about.title("About the UC Berkeley CS9H Turtle Arena")
        about.geometry("400x400")
        Message(about, text="Tom and Jerry Simulator",width=200).pack()
        Message(about, text="by").pack()
        Message(about, text="Morten Wehlast Jørgensen",width=200).pack()
        myPic = PhotoImage(file="Morten.gif")
        l = Label(about, image = myPic)
        l.pack(side = "top")
        l.photo = myPic #Keep reference for image
        button = Button(about, text='OK', command=about.destroy)
        button.pack(side = "top")

    def press(self, event):
        dragstart = Vector(event.x, event.y)
        for turtle in self.turtles:
            if (dragstart - turtle.position).length() < 10:
                self.dragging = turtle
                self.dragstart = dragstart
                self.start = turtle.position
                return

    def motion(self, event):
        drag = Vector(event.x, event.y)
        

        if self.dragging:
            self.dragging.position = self.start + drag - self.dragstart
            
            if self.dragging.type == "Cat": #Check if a cat is being dragged
                self.dragging.style['fill'], self.dragging.style['outline'] = black, black #Blacken cat
                self.update(self.dragging)
                self.dragging.angle = (self.dragging.position - self.dragging.anchor).direction()
                self.dragging.heading = self.dragging.angle - 180 #Turn towards statue
                self.dragging.radius = (self.dragging.position - self.dragging.anchor).length()*px2m
                
                if self.dragging.radius < 1: #Make sure cat is not inside statue
                    self.dragging.radius = 1
                    self.dragging.position = self.dragging.anchor + unit(self.dragging.angle)*m2px
            
            #Update labels
            self.catAngle.set('CatAngle: {0:.1f}'.format(self.dragging.angle))
            self.catRadius.set('CatRadius: {0:.3f}'.format(self.dragging.radius))
            self.update(self.dragging)
            
        else:
            for turtle in self.turtles:
                if turtle.type == "Cat": #Give cat its original colors back
                    turtle.style['fill'], turtle.style['outline'] = turtle.origFill, turtle.origOutline
                    self.update(turtle)
                
    def release(self, event):
        self.dragging = None

    def update(self, turtle):
        """Update the drawing of a turtle according to the turtle object."""
        item = self.items[turtle]
        vertices = [(v.x, v.y) for v in turtle.getshape()]
        self.canvas.coords(item, sum(vertices, ()))
        self.canvas.itemconfigure(item, **turtle.style)

    def add(self, turtle):
        """Add a new turtle to this arena."""
        self.turtles.append(turtle)
        self.items[turtle] = self.canvas.create_polygon(0, 0)
        self.update(turtle)

    def step(self, stop=1):
        """Advance all the turtles one step."""
        
        self.time += self.period
        self.timeText.set('Time: {0:.2f}'.format(self.time/1000))
        
        
        nextstates = {}
        for turtle in self.turtles:
            nextstates[turtle] = turtle.getnextstate()
        for turtle in self.turtles:
            turtle.setstate(nextstates[turtle])
            self.update(turtle)
            #Update labels as well
            if turtle.type == "Cat":
                self.catAngle.set('CatAngle: {0:.1f}'.format(turtle.angle))
                self.catRadius.set('CatRadius: {0:.3f}'.format(turtle.radius*px2m))
                
            if turtle.type == "Mouse":
                self.mouseAngle.set('MouseAngle: {0:.1f}'.format(turtle.angle))
                
        if stop:
            self.running = 0
        
        
        

    def run(self):
        """Start the turtles running."""
        self.running = 1
        self.loop()

    def loop(self):
        """Repeatedly advance all the turtles one step."""
        self.step(0)
        if self.running:
            self.tk.createtimerhandler(self.period, self.loop)

    def stop(self):
        """Stop the running turtles."""
        self.running = 0
    
    def get_timestamp(self):
        return self.time
    
    def reset(self):
        """Reset entire simulation into original specified by the user"""
        self.running = 0
        self.time = 0
        self.timeText.set('Time: '+str(self.time))
        nextstates = {}
        
        for turtle in self.turtles:
            nextstates[turtle] = turtle.reset()
        
        for turtle in self.turtles:
          turtle.setstate(nextstates[turtle])
          self.update(turtle)
            
            
            
            