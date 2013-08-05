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
	
	#start adding points
	def start(points = []):
		mainWindow.onExit()
		QuickHull(points) #Start QuickHull process
		mainWindow.mainloop();
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
				start(points) #Start QuickHull process

		ok = Button(AskFile,width=10, text="OK", command=readin)
		ok.place(x=70,y=70)
		fileWindow.startLoop() 

	menubar = Menu(Panel)
	Panel.config(menu=menubar)

	fileMenu = Menu(menubar)
	#fileMenu.add_command(label="Start", command = start)

	fileMenu.add_command(label="Import...", command = getFile)
	fileMenu.add_command(label="Exit", command = mainWindow.onExit)
	menubar.add_cascade(label="File",menu=fileMenu)

	SButton = Button(Panel, text = "Start", command = start)
	SButton.pack()

	mainWindow.startLoop()
#==================================Draw Stuff======================================


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