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
import threading
from time import sleep

#custom imports
import Triangles
from window import Window

class QuickHull(Tk):
	start = True
	first = True

	def __init__(self,points):
		Tk.__init__(self)
		board = Frame(self)
		self.title("Diagram") 

		width = 800 #setting height and width
		height = 600

		windowx = self.winfo_screenwidth()
		x = (windowx - width)		#getting top right 
		y = 0

		self.geometry("%dx%d+%d+%d" % (width,height,x,y)) #creates window of size _width by _height, and positions it at the center of the screen

		board.pack(fill=BOTH, expand=1)
	
		self.canvas = Canvas(board,height=600,width=800)
		self.canvas.place(x=0,y=0)
		maxY = 0
		minY = 600
		for p in points:
			if p[1] > maxY:
				maxY = p[1]
				q = p
			if p[1] < minY:
				minY = p[1]
				r = p
	
		self.drawPoints(points,r,q) #Draw points and the first line from the highest an lowest points
		
		points.remove(r)
		points.remove(q)
		
		self.points = points 				#Initialize Attributes
		self.r = r
		self.q = q
		self.furthestPoint = q

		self.nextButton()			

		[set0,set1] = Triangles.splitPoints(self.r,self.furthestPoint,self.q,self.points)

		self.points = set0
		self.animate()
		self.points = set1
		self.animate()

		self.mainloop()

		self.onExit()
			
	def nextButton(self):					#Button that starts and stops animation
		def callBack():
			self.start = not self.start
			if(self.start):
				continueB["text"] = "Stop"
			else:
				continueB["text"] = "Start"

		continueB = Button(self, text="Start",command=callBack)
		continueB.place(x=350,y=550)

	def animate(self):						#animation loop
		if self.start:
			self.qhalg(self.r,self.q,self.points)
			[set0,set1] = Triangles.splitPoints(self.r,self.furthestPoint,self.q,self.points)
			[set0,set2] = Triangles.splitPoints(self.furthestPoint,self.q,self.r,self.points)

			r = self.r
			q = self.q
			furthestPoint = self.furthestPoint

			if(len(set1) > 0):
				self.points = set1
				self.qhalg(r,furthestPoint,set1)
				self.after(1000, self.animate)
			if(len(set2) > 0):
				self.points = set2
				self.qhalg(r,furthestPoint,set2)
				self.after(1000, self.animate)
			return




	def onExit(self):
		alert = Tk()
		finish = Window(alert)
		finish.config(title="Complete",w = 200, h=50)
		finish.positionWindow()

		done = Label(alert,text="QuickHull Complete")
		done.pack()

		ok = Button(alert,text="OK",command=alert.destroy)
		ok.pack()
		alert.mainloop()

	def qhalg(self,r,q,points):
		furthestPoint = []       #In the inital call q and r two points with the highest and lowest y(or x) value
		maxdist = -1

		if points == []:
			return [],[]

		for p in points:
			temp = sqrt((r[0] - p[0])**2 + (r[1] - p[1])**2) + sqrt((q[0] - p[0])**2 + (q[1] - p[1])**2)  #distance of p from q and p added together
			if(temp > maxdist):
				furthestPoint = p   #finds the furthest point from the line r, q
				maxdist = temp

		if(furthestPoint == []):
			return [],[]
				
		triangle = r + q + furthestPoint
		self.drawTriangle(triangle,)

		self.q = q
		self.r = r
		self.furthestPoint = furthestPoint

#==================================Animate Triangles=========================================

	def drawTriangle(self,triangle):		 #draw triangle
		#self.canvas.create_polygon(triangle,fill='red',outline="black")
		self.canvas.create_line(triangle[0],triangle[1],triangle[2],triangle[3],fill="black")
		self.canvas.create_line(triangle[2],triangle[3],triangle[4],triangle[5],fill="black")
		self.canvas.create_line(triangle[4],triangle[5],triangle[0],triangle[1],fill="black")

	def drawPoints(self,points,q,r):			#Draw points and initial line
		for p in points:
			self.canvas.create_text(p[0],p[1],text="+")
		self.canvas.create_line(r[0],r[1],q[0],q[1],fill="black")


"""
#======================================Thread==========================================
class QuickThread(threading.Thread):
	results = []
	def __init__(self,r,q,points,canvas):
		threading.Thread.__init__(self)
		self.r = r
		self.q = q
		self.points = points
		canvas = canvas


	def run(self): #takes a set of points and line and finds all of the outer points

		if self.points == []:
			self.results = False
		else:			
			sleep(sleeptime)
			self.results=[self.qhalg(self.r,self.q,self.points)]
		return
		

	def qhalg(self,r,q,points):
		furthestPoint = []       #In the inital call q and r two points with the highest and lowest y(or x) value
		maxdist = -1

		if points == []:
			return False

		for p in points:
			temp = sqrt((r[0] - p[0])**2 + (r[1] - p[1])**2) + sqrt((q[0] - p[0])**2 + (q[1] - p[1])**2)  #distance of p from q and p added together
			if(temp > maxdist):
				furthestPoint = p   #finds the furthest point from the line r, q
				maxdist = temp

		if(furthestPoint == []):
			return False
		
		
		
		triangle = r + q + furthestPoint
		self.drawTriangle(triangle)

		[set0,set1] = Triangles.splitPoints(r,furthestPoint,q,points)
		[set0,set2] = Triangles.splitPoints(q,furthestPoint,r,points)


		return set1, set2, furthestPoint

#==================================Animate Triangles=========================================

	def drawTriangle(self,triangle):
		
		self.canvas.create_polygon(triangle,fill='red',outline="black")


#===============================Start Window============================================
def start(points):		
	draw = Tk()

	board = Window(draw)
	board.config(title = "Diagram")
	board.positionWindow(board.TOPRIGHT)

	canvas = Canvas(draw,height=600,width=800)
	canvas.place(x=0,y=0)
	maxY = 0
	minY = 600
	for p in points:
		if p[1] > maxY:
			maxY = p[1]
			q = p
		if p[1] < minY:
			minY = p[1]
			r = p

	drawPoints(canvas,points,r,q) #Draw points and the first line from the highest an lowest points

	points.remove(r)
	points.remove(q)

	[set1,set2] = Triangles.splitPoints(r,q,q,points)

	qh = QuickHull(draw,canvas) 
	qh.start(r,q,set1)

	while qh.done == False:
		pass

	qh.done = False	
	qh.start(r,q,set2)
	while qh.done == False:
		pass

"""
"""
	def threadManger(self,thread):

		thread.start()
		set1=[]
		set2=[]
		furthestPoint = []

		print ("Start")
		while True:
			try:
				print ("In Loop")
				[set1,set2,furthestPoint] = thread.results
			except ValueError:
				if thread.results == False:
					print ("No results returned")
					break

			finally:
				break
		#self.hull.insert(self.hull.index(thread.q),furthestPoint)

		if(len(set1) > 0):
			print ("Set1 is valid")
			newThread = QuickThread(thread.r,furthestPoint,set1,thread.canvas)
			self.threadManger(newThread)
		#	self.hull = hull[:hull.index(r)]+temp+hull[hull.index(furthestPoint):] 
		if(len(set2) > 0):
			print ("Set2 is valid")
			newThread = QuickThread(furthestPoint,thread.q,set2,thread.canvas)
			self.threadManger(newThread)

		return True
"""	 	
#==============================End of QH Object========================================