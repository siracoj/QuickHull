"""
QuickHull Object

This object manages the threads created
by each iteration of QuickHull

Author: Jared Siraco
"""
#imports
from math import sqrt
from tkinter import ttk,Tk,Frame,Menu,Canvas,BOTH
from tkinter.ttk  import *

#custom imports
import Triangles
from window import Window

triList = []

class QuickHull(Tk):
	def __init__(self,points):
		Tk.__init__(self)
		board = Frame(self)
		self.title("Diagram") 

		width = 800 #setting height and width
		height = 600

		windowx = self.winfo_screenwidth()
		windowy = self.winfo_screenheight()
		x = (windowx - width)/2		#getting center
		y = (windowy - height)/2

		self.geometry("%dx%d+%d+%d" % (width,height,x,y)) #creates window of size _width by _height, and positions it at the center of the screen

		board.pack(fill=BOTH, expand=1)
	
		self.canvas = Canvas(board,height=600,width=800,background="white")
		self.canvas.place(x=0,y=0)
		
		self.drawPoints(points) #Draw points and the first line from the highest an lowest points
		

					

		
		def point(event):  #Add points by clicking on the screen
			self.canvas.create_text(event.x, event.y,text = "+")
			points.append([event.x,event.y])

		def start():
			if(points != []):
				startB.destroy()
				quickHullStart(points)
				self.nextButton()
	
		self.canvas.bind("<Button-1>", point)
		
		startB = Button(self, text = "Start QuickHull", command = start)
		startB.pack()
	
		
	
		self.mainloop()
	
				
	def nextButton(self):					#Button that steps forward one step in the QuickHull
		def callBack():
			self.animate()

		continueB = Button(self, text="-->",command=callBack)
		continueB.place(x=350,y=550)


	def animate(self):						#animation loop
		if(triList == []):
			self.onExit()
			return
		self.canvas.create_polygon(triList.pop(0),fill="red",outline="black")
			





	def onExit(self):  #Window popup signaling that the Quick Hull is complete
		alert = Tk()
		finish = Window(alert)
		finish.config(title="Complete",w = 200, h=50)
		finish.positionWindow()

		done = Label(alert,text="QuickHull Complete")
		done.pack()

		ok = Button(alert,text="OK",command=alert.destroy)
		ok.pack()
		alert.mainloop()
		return
		


	def drawPoints(self,points):			#Draw points Imported from a file
		for p in points:
			self.canvas.create_text(p[0],p[1],text="+")
		



def quickHullStart(points):  #Setup for the QuickHull Algorithm
	maxY = -1
	minY = float('inf')
	for p in points:  #getting highest and lowest points (r, q)
		if p[1] > maxY:
			maxY = p[1]
			q = p
		if p[1] < minY:
			minY = p[1]
			r = p
		
	points.remove(r)
	points.remove(q)
	hull = r+q
	
	[set0,set1] = Triangles.splitPoints(r,q,q,points)  #Spliting points in half by a line with the Highest and lowest points
	
	quickHullAlg(set0, r,q)
	quickHullAlg(set1, r,q)

def quickHullAlg(points, r, q):	
	furthestPoint = []       #In the inital call q and r two points with the highest and lowest y value
	maxdist = -1

	if points == []:
		return

	if len(points) == 1:
		furthestPoint = points

	for p in points:
		temp = sqrt((r[0] - p[0])**2 + (r[1] - p[1])**2) + sqrt((q[0] - p[0])**2 + (q[1] - p[1])**2)  #distance of p from q and p added together
		if(temp > maxdist):
			furthestPoint = p   #finds the furthest point from the line r, q
			maxdist = temp

	if(furthestPoint == []):
		return
	points.remove(furthestPoint)
			
	triangle = r + q + furthestPoint
	triList.append(triangle) #adding a triangle to the set to print out

	[set0,set1] = Triangles.splitPoints(r,furthestPoint,q,points)
	[set0,set2] = Triangles.splitPoints(q,furthestPoint,r,points)
		
	quickHullAlg(set1,r,furthestPoint)
	quickHullAlg(set2,furthestPoint, q)

