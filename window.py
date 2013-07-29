"""
Simple window class

This is an object represents a window, 
providing common initialization functions
and options

Author: Jared Siraco
"""


from tkinter import *
from tkinter.ttk import *


class Window(Frame):

	CENTER = 0		#Built in Position Values
	CENTERLEFT = 1
	CENTERRIGHT = 2
	TOP = 3
	TOPLEFT = 4
	TOPRIGHT = 5
	BOTTOM = 6
	BOTTOMLEFT = 7
	BOTTOMRIGHT = 8

	def __init__(self, parent):
		Frame.__init__(self,parent)

		self.parent = parent #Reference to the parent widget(The frame)
		
		self._isStarted = False

		self._width = 800 #setting default _height and _width(psudo private variables)
		self._height = 600

	def config(self, title = "default", w = 800, h=600, color="white"):		
		self._initUI(w,h,title)  #creation of the user interface
		
	def _initUI(self,w,h,title): #psudo private method
		self.setTitle(title) 

		self._width = w #setting default _height and _width(psudo private variables)
		self._height = h 

		self.style = Style()
		self.style.theme_use("default")

	def positionWindow(self, position=0): #Call after setting dimentions and before widget additions
		if(self._isStarted):
			print("Cannot set geometry while running")
			return

		windowx = self.parent.winfo_screenwidth()  #getting _height and _width of screen
		windowy = self.parent.winfo_screenheight()

		if(position == self.TOP):
			x = (windowx - self._width)/2		#getting top 
			y = 0
		elif(position == self.TOPRIGHT):
			x = (windowx - self._width)		#getting top right 
			y = 0
		elif(position == self.TOPLEFT):
			x = 0								#getting top left 
			y = 0
		elif(position == self.CENTERRIGHT):
			x = (windowx - self._width)		#getting center right osition
			y = (windowy - self._height)/2
		elif(position == self.CENTERLEFT):
			x = 0								#getting center left psition
			y = (windowy - self._height)/2
		elif(position == self.BOTTOMLEFT):
			x = 0								#getting bottom left psition
			y = (windowy - self._height)
		elif(position == self.BOTTOMRIGHT):
			x = (windowx - self._width)		#getting bottom right osition
			y = (windowy - self._height)
		elif(position == self.BOTTOM):
			x = (windowx - self._width)/2		#getting bottom positin
			y = (windowy - self._height)
		else:
			x = (windowx - self._width)/2		#getting center positin(default)
			y = (windowy - self._height)/2

		self.parent.geometry("%dx%d+%d+%d" % (self._width,self._height,x,y)) #creates window of size _width by _height, and positions it at the center of the screen

		self.pack(fill=BOTH, expand=1)


	def setDimentions(self,w,h): #change size of the window
		if(self._isStarted):
			print("Cannot change dimentions while running")
			return

		self._width = w
		self._height = h

	def setTitle(self,title):		#sets the title
		if(self._isStarted):
			print("Cannot change title while running")
			return

		self.parent.title(title)

	def startLoop(self):			#starts the Frame
		if(self._isStarted):
			print("Frame already started")
			return
		self._isStarted = True
		self.parent.mainloop()

	def onExit(self):			   #Exits the window
		if(self._isStarted == False):
			print("Frame Is not runnning")
			return
		self._isStarted = False
		self.parent.destroy()



