"""
QuickHull Animation

This is a program that takes a set of points choosen by the user
and ether animates the QuickHull process or the user can click through it step by step

Author: Jared Siraco
"""

#imports
from tkinter import ttk,Tk,Frame,Menu,Canvas
from tkinter.ttk  import *
import threading

#Custom imports
from window import Window
import Triangles
from QuickHull import QuickHull



#==========================================GUI=======================================
def startWindow():
	points = []
	Panel = Tk()

	mainWindow = Window(Panel)
	mainWindow.config(title = "QuickHull Menu",h=150,w=200)
	mainWindow.positionWindow(mainWindow.TOPLEFT)
	
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
		qh.start(r,q,set2)

	#start adding points
	def exportData():
		return
	#Export points to csv
	def getFile():

		AskFile = Tk()

		fileWindow = Window(AskFile)
		fileWindow.config(title="Import...", w=200, h=100)
		fileWindow.positionWindow(fileWindow.TOPLEFT)

		ask = Label(AskFile, text = "What file would you like to import? ")
		ask.place(x=10,y=25)

		style = Style()
		style.configure("BW.TEntry", foreground="black", background="white")

		text = Entry(AskFile,width=29,style="BW.TEntry")  #Create Text Box
		text.place(x=10,y=45)
		text.focus_set()

		def readin(): #Call back to get text, open the file, and close the window
			try:
				print ("Loading file...")
				filename = text.get()
				if(filename==""):
					filename = "test.txt"		#uses test as default entry
				data = open(filename)
				points = [[int(x) for x in line.split()] for line in data] # takes a each point in as: x y 

				fileWindow.onExit()
			except IOError:
				print ("Could not read the specified file")
			finally:
				print("Closing Import...")
				start(points)

		ok = Button(AskFile,width=10, text="OK", command=readin)
		ok.place(x=70,y=70)
		fileWindow.startLoop() 

	menubar = Menu(Panel)
	Panel.config(menu=menubar)

	fileMenu = Menu(menubar)
	fileMenu.add_command(label="Start", command = start)
	fileMenu.add_command(label="Export points", command = exportData)
	fileMenu.add_command(label="Import...", command = getFile)
	fileMenu.add_command(label="Exit", command = mainWindow.onExit)
	menubar.add_cascade(label="File",menu=fileMenu)

	mainWindow.startLoop()
#==================================Draw Stuff======================================
def drawPoints(canvas,points,q,r):
	for p in points:
		canvas.create_text(p[0],p[1],text="+")
	canvas.create_line(r[0],r[1],q[0],q[1],fill="purple")

def drawPolygon(self):
	poly = []
	for x in self.hull:
		poly += x
	self.canvas.create_polygon(poly,fill='black',outline="purple")

#===================================Main===========================================


def main():
	print ("Starting Application...")
	startWindow()

main()