from libdw import sm

class Fruit:
    def relativeMovement(self):
        return (self.relativeRotation, self.unitsForward)
        
class Apple(Fruit):
    relativeRotation = 0
    unitsForward = 1

class Pear(Fruit):
    relativeRotation = -90
    unitsForward = 0

class Plum(Fruit):
    relativeRotation = 90
    unitsForward = 0
    
class Herbivore(sm.SM):
    def __init__(self, startState="east"):
        self.startState = startState
        self.pos = (0,0)
    
    def getNextValues(self,state,inp):
        if state == "east":
            if isinstance(inp, Apple):
                nextState = "east"
                outp = (self.pos[0]+1,self.pos[1])
            if isinstance(inp, Pear):
                nextState = "north"
                outp = self.pos
            if isinstance(inp, Plum):
                nextState = "south"
                outp = self.pos

        if state == "south":
            if isinstance(inp, Apple):
                nextState = "south"
                outp = (self.pos[0],self.pos[1]-1)
            if isinstance(inp, Pear):
                nextState = "east"
                outp = self.pos
            if isinstance(inp, Plum):
                nextState = "west"
                outp = self.pos
                
        if state == "west":
            if isinstance(inp, Apple):
                nextState = "west"
                outp = (self.pos[0]-1,self.pos[1])
            if isinstance(inp, Pear):
                nextState = "south"
                outp = self.pos
            if isinstance(inp, Plum):
                nextState = "north"
                outp = self.pos
                
        if state == "north":
            if isinstance(inp, Apple):
                nextState = "north"
                outp = (self.pos[0],self.pos[1]+1)
            if isinstance(inp, Pear):
                nextState = "west"
                outp = self.pos
            if isinstance(inp, Plum):
                nextState = "east"
                outp = self.pos
        
        self.pos = outp
        return nextState, outp
        
fruits = [Apple(), Apple(), Pear(), Apple(), Pear(), Apple()]