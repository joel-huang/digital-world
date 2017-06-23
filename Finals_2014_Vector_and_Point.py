import math

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return 'Point2D('+str(self.x)+','+str(self.y)+')'
    def add(self, vect):
        self.x += vect.dx
        self.y += vect.dy
        return self.__str__()
        

class Vector2D:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        
    def length(self):
        return math.sqrt(self.dx**2 + self.dy**2)
        
class Polyline2D:
    def __init__(self, point, veclist):
        self.point = point
        self.veclist = veclist
        self.lenTotal = 0

    def addSegment(self,lineSegment):
        self.veclist.append(lineSegment)
    
    def length(self):
        for i in self.veclist:
            self.lenTotal += i.length()
        return self.lenTotal
        
    def vertex(self,index): # index 1 @ intersection of first and second line seg.
        if index == 0:
            return self.point
        elif index >= 1:
            self.point.x += self.veclist[index-1].dx
            self.point.y += self.veclist[index-1].dy
            return self.point
            
class ClosedPolyline2D(Polyline2D):
    def length(self):
        vertList = []
        for i in self.veclist:
            self.lenTotal += i.length()
        for j in range(len(self.veclist)+1):
            x = self.vertex(j)
            vertexCoordinate = (x.x,x.y)
            vertList.append(vertexCoordinate)
        
        firstPoint = vertList[0]
        lastPoint = vertList[-1]
        
        addLength = math.sqrt((lastPoint[0]-firstPoint[0])**2+(lastPoint[1]-firstPoint[1])**2)
        
        return self.lenTotal+addLength
    
            
pline = Polyline2D(Point2D(1,2),[Vector2D(3,1)])
pline.addSegment(Vector2D(1,0))
pline.addSegment(Vector2D(0,2))

print pline.length()

print pline.vertex(0)
print pline.vertex(1)
print pline.vertex(2)
print pline.vertex(3)