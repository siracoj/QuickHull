"""
QuickHull Animation

This is a program that takes a set of points choosen by the user
and ether animates the QuickHull process or the user can click through it step by step

Author: Jared Siraco
"""

#imports
from __future__ import division
from math import sqrt
from tkinter import ttk,Tk,Frame,Menu,Canvas
from tkinter.ttk  import *
import threading

#Custom imports
from window import Window
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

		drawPoints(canvas,points)

		points.remove(r)
		points.remove(q)

		click = threading.Event()

		qh = QuickHull(click,draw,canvas)
		

		def continues():
			click.set()
		
		next = Button(Panel,text="-->",command=continues)
		next.place(x=50,y=100)

		draw.mainloop()

		qh.start(r,q,points)

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
				filename = "test.txt"		#uses test as default entry
				filename = text.get()
				
				data = open(filename)
				points = [[int(x) for x in line.split()] for line in data]
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

def drawPoints(canvas,points):
	for p in points:
		canvas.create_text(p[0],p[1],text="+")

#===================================Main===========================================


def main():
	print ("Starting Application...")
	startWindow()

main()