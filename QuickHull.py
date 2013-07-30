"""
QuickHull Object

This object manages the threads created
by each iteration of QuickHull

Author: Jared Siraco
"""
#imports
from math import sqrt
from tkinter import ttk,Tk,Frame,Menu,Canvas
from tkinter.ttk  import *
import threading

#custom imports
import Triangles
from window import Window

class QuickHull(Frame):
	hull = []

	def __init__(self,parent,canvas):
		Frame.__init__(self,parent)

		self.parent = parent
		self.canvas = canvas

		self.nextButton()
		
	def nextButton(self):
		def callBack():
			try:
				threadLock.release()
			except RuntimeError:
				print("Thread Busy")
		continueB = Button(self.parent, text="-->",command=callBack)
		continueB.place(x=350,y=550)


	def start(self,r,q,points):

		hull = r + q

		thread = QuickThread(r,q,points,self.canvas)

		self.threadManger(thread)


	def threadManger(self,thread):

		thread.start()
		set1=[]
		set2=[]

		while True:
			try:
				[set1,set2,furthestPoint] = thread.results
			except ValueError:
				if thread.results == False:
					break
			finally:
				break
		#self.hull.insert(self.hull.index(thread.q),furthestPoint)

		if(len(set1) > 0):
			newThread = QuickThread(thread.r,furthestPoint,set1,thread.canvas)
			threadLock.acquire(1)
		#	self.hull = hull[:hull.index(r)]+temp+hull[hull.index(furthestPoint):] 
		if(len(set2) > 0):
			newThread = QuickThread(furthestPoint,thread.q,set2,thread.canvas)
			threadLock.acquire(1)
			self.threadManger(newThread)
	 	

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

#======================================Thread==========================================
class QuickThread(threading.Thread):
	results = []
	def __init__(self,r,q,points,canvas):
		threading.Thread.__init__(self)
		self.r = r
		self.q = q
		self.points = points
		self.canvas = canvas


	def run(self): #takes a set of points and line and finds all of the outer points

		if self.points == []:
			return
		threadLock.acquire(1)
		results=[self.qhalg(self.r,self.q,self.points)]
		while results == []:
			pass
		

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





#==============================End of QH Object========================================
threadLock = threading.Lock() #GLobal Lock
count = 0