#imports
from __future__ import division
from math import sqrt
from tkinter import ttk,Tk,Frame,Menu,Canvas
from tkinter.ttk  import *
from time import sleep
from window import Window
import threading
class QuickThread(threading.Thread):
	def __init__(self,r,q,points, qh):
		self.r = r
		self.q = q
		self.points = points
		self.qh = qh

	def run(self): #takes a set of points and line and finds all of the outer points

		if points == []:
			return
		qh.qhalg(self.r,self.q,self.points)


class QuickHull:
	hull = []
	count = 0
	triangle = []
	done = False

	def __init__(self,parent,Panel,canvas):
		self.parent = parent
		self.Panel = Panel
		self.canvas = canvas

	def start(self,r,q,points):

		self.hull=[r,q]

		[side1,side2] = self.splitPoints(r,q,points[0],points)
		thread1 = QuickThread(r,q,side1,self)
		thread2 = QuickThread(r,q,side2,self)

		thread1.start()
		thread1.join()
		
		thread2.start()
		thread2.join()

		self.onExit()

	def splitPoints(self,r,q,testpoint,points):
		side1 = points[0]
		side2 = []

		for p in points:
			if(sameSide(p,testpoint,r,q)):
				side1.append(p)
			else:
				side2.append(p)

		return side1, side2
	 	
	def qhalg(self,r,q,points):
		furthestPoint = []       #In the inital call q and r two points with the highest and lowest y(or x) value
		maxdist = -1

		if points == []:
			return
		print("1")

		try:
			for p in points:
				temp = sqrt((r[0] - p[0])**2 + (r[1] - p[1])**2) + sqrt((q[0] - p[0])**2 + (q[1] - p[1])**2)  #distance of p from q and p added together
				if(temp > maxdist):
					furthestPoint = p   #finds the furthest point from the line r, q
					maxdist = temp
		except TypeError:
			furthestPoint = points

		if(furthestPoint == []):
			return False
		
		self.hull.insert(self.hull.index(q),furthestPoint)
		
		self.triangle = r + q + furthestPoint
		self.drawPolygon()

		[set0,set1] = self.splitPoints(r,furthestPoint,q,points)
		[set0,set2] = self.splitPoints(q,furthestPoint,r,points)

		self.parent.clear()
		self.run(r,furthestPoint,set1)
		self.parent.clear()
		self.run(furthestPoint,q,set2)


		return furthestPoint
	#==================================Animate=========================================

	#def drawLine(canvas,r,q,color):
	#canvas.create_line(r[0],r[1],q[0],q[1],fill=color)
	def drawPolygon(self):
		poly = []
		for x in self.hull:
			poly += x

		self.canvas.create_polygon(poly,fill='black')
	def drawTriangle(self):
		if(self.count == 0):
			self.canvas.create_polygon(self.triangle,fill='blue')
			self.count += 1
		elif(self.count == 1):
			self.canvas.create_polygon(self.triangle,fill='red')
			self.count += 1
		elif(self.count == 2):
			self.canvas.create_polygon(self.triangle,fill='green')
			self.count += 1
		else:
			self.canvas.create_polygon(self.triangle,fill='black')
			self.count = 0

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

		hull = []
		count = 0
		triangle = []
		points = []




#==============================End of QH Object========================================

def inTriangle(p, t1,t2,t3): #Checking if p is in the triangle furthestPoint,q,r
	if(sameSide(p,t1, t2,t3) and sameSide(p,t2, t1,t3) and sameSide(p,t3, t2,t1)):  
		return True
	else:
		return False

def sameSide(p1,p2, q,r): #Determines if point p1 is on the same side of the line from q to r as p2
	cp1 = crossProduct([r[0]-q[0], r[1]-q[1], 0], [p1[0]-q[0], p1[1]-q[1], 0])
	cp2 = crossProduct([r[0]-q[0], r[1]-q[1], 0], [p2[0]-q[0], p2[1]-q[1], 0])
	if((cp1[0]*cp2[0] + cp1[1]*cp2[1] + cp1[2]*cp2[2]) >= 0):
		return True
	else:
		return False

def crossProduct(vec1, vec2): #Preforms cross product on 3 dimentional vectors
	result = []

	result.append(vec1[1]*vec2[2] - vec2[1]*vec1[2])
	result.append(vec1[2]*vec2[0] - vec2[2]*vec1[0])
	result.append(vec1[0]*vec2[1] - vec2[0]*vec1[1])

	return result