"""
Triangles

A few functions that determine a points location
relative to a triangle
Author: Jared Siraco
"""

def splitPoints(r,q,testpoint,points): #splits points between points on the same side
	side1 = [points[0]]				   #as testpoint and those not
	side2 = []

	for p in points:
		if(sameSide(p,testpoint,r,q)):
			side1.append(p)
		else:
			side2.append(p)

	return side1, side2

def inTriangle(p, t1,t2,t3): #Checking if p is in the triangle t
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