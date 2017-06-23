# The Digital World - Final Exam 2016
# Great exercise on classes using an Avatar to navigate a Map with different events at specific coordinates.

import copy
from libdw import sm

class Avatar(object):
    
    def __init__(self,name,hp=100,position=(1,1)):
        self.name = name
        self.hp = hp
        self.position = position
        
    def getName(self):
        return self.name
        
    def setName(self, name):
        self.name = name
        
    def getHP(self):
        return self.hp
        
    def setHP(self, hp):
        self.hp = hp
        
    def getPosition(self):
        return self.position
        
    def setPosition(self,position):
        self.position = position
        
    def heal(self,amount=1):
        if amount > 0:
            afterHeal = self.hp + amount
            self.setHP(afterHeal)
        else:
            None
            
    def attacked(self,amount=-1):
        if amount < 0:
            afterDamage = self.hp + amount
            self.setHP(afterDamage)
        else:
            None

class Map(object):
    def __init__(self,world):
        self.world = copy.deepcopy(world)
    
    def whatIsAt(self,position):
        # check if tuple is key in dic
        if position in self.world:
            if type(self.world[position]) == str and self.world[position] == 'x':
                return 'Exit' #if it is a character ‘x’, the function should return a string ‘Exit’
            if type(self.world[position]) == int and self.world[position] == 0:
                return 'Wall' #if it is an integer 0, the function should return a string ‘Wall’
            if type(self.world[position]) == int and self.world[position] > 0:
                return 'Food' #if it is a positive integer, the function should return a string ‘Food’
            if type(self.world[position]) == int and self.world[position] < 0:
                return 'Enemy' #if it is a negative integer, the function should return a string ‘Enemy’
        else:
            return 'Empty' #if it is not found in the world dictionary, the function should return a string ‘Empty’.
    
    def getEnemyAttack(self,position):
        if self.whatIsAt(position) == 'Enemy':
            return self.world[position]
        else:
            return False
        
    def getFoodEnergy(self,position):
        if self.whatIsAt(position) == 'Food':
            return self.world[position]
        else:
            return False
            
    def removeEnemy(self,position):
        if self.whatIsAt(position) == 'Enemy':
            del self.world[position]
            return True
        else:
            return False
            
    def eatFood(self,position):
        if self.whatIsAt(position) == 'Food':
            del self.world[position]
            return True
        else:
            return False
            
    def getExitPosition(self):
        x = None
        for i in self.world:
            if self.world[i] == 'x':
                x = i
        return x        
        
class DW2Game(sm.SM):
    def __init__(self,avatarObj,mapObj):
        self.startState = (copy.deepcopy(avatarObj),copy.deepcopy(mapObj))
        
    def getNextValues(self,state,inp): # nextState=(avatarState,mapState) inp = (action,direction)
        
        nextState = copy.deepcopy(state)
        
        avatarState = nextState[0]
        mapState = nextState[1]
            
        if inp[1] == 'up':
            upY = (avatarState.position[1]-1)
            newPos = (copy.deepcopy(avatarState.position[0]),upY)
        elif inp[1] == 'down':
            downY = (avatarState.position[1]+1)
            newPos = (copy.deepcopy(avatarState.position[0]),downY)
        elif inp[1] == 'left':
            downX = (avatarState.position[0]-1)
            newPos = (downX,copy.deepcopy(avatarState.position[1]))
        elif inp[1] == 'right':
            upX = (avatarState.position[0]+1)
            newPos = (upX,copy.deepcopy(avatarState.position[1]))
            
        if inp[0] == 'move': #set the new position
            if mapState.whatIsAt(newPos) in ['Empty','Food','Exit']:
                avatarState.position = newPos
                if mapState.whatIsAt(newPos) == 'Food':
                    avatarState.heal(mapState.getFoodEnergy(newPos))
                    mapState.eatFood(newPos)
            elif mapState.whatIsAt(newPos) == 'Enemy':
                avatarState.attacked(mapState.getEnemyAttack(newPos))
            
        if inp[0] == 'attack':
            if mapState.whatIsAt(newPos) == 'Enemy':
                mapState.removeEnemy(newPos)

        return (avatarState,mapState),(avatarState.name,avatarState.position,avatarState.hp)


# Test Cases
print 'Question 7 Test Cases \n'

world2={(0,0):0, (1,0):0 , (2,0):0, (3,0): 0, (4,0):0, (5,0): 0, (0,1):0, (5,1): 0, (0,2):0, (1,2): -2, (5,2): 0, (0,3):0, (2,3): 3, (5,3): 0, (0,4):0, (5,4): 0, (0,5):0, (1,5):0, (2,5):0, (3,5): 0, (4,5):'x', (5,5): 0,}

print 'test 1'
inp = [('move','down'),('attack','down'),('move','down'),('move','down'),('move','down'),('move','right'),('move','right'),('move','right'),('move','down'),('move','down')]
av = Avatar('John')
m = Map(world2)
g = DW2Game(av,m)
print g.transduce(inp)

print 'test 2'
inp=[('move','left'),('move','right'),('move','right'),('move','right'),('move','right'),('move','down'),('move','down'),('move','down'),('move','up')]
av=Avatar('John')
m=Map(world2)
g=DW2Game(av,m)
print g.transduce(inp)

print 'test 3'
inp=[('move','right'),('move','right'),('move','right'),('move','down'),('move','left'),('move','left'),('move','left'),('attack','left'),('move','left')]
av=Avatar('John')
m=Map(world2)
g=DW2Game(av,m)
print g.transduce(inp)

print 'test 4'
inp=[('move','right'),('move','right'),('move','right'),('move','down'),('move','left'),('move','left'),('move','left'),('attack','left'),('move','left'),('move','left'),('move','down'),('move','right')]
av=Avatar('John')
m=Map(world2)
g=DW2Game(av,m)
print g.transduce(inp)

print 'test 5'
inp=[('move','right'),('move','right'),('move','right'),('move','down'),('move','left'),('move','left'),('move','left'),('attack','left'),('move','left'),('move','left'),('move','down'),('move','right'),('move','right'),('move','right'),('move','down'),('move','down'),('move','down')]
av=Avatar('John')
m=Map(world2)
g=DW2Game(av,m)
print g.transduce(inp)

print 'test 6'
av=Avatar('John')
m=Map(world2)
g=DW2Game(av,m)
g.start()
n,o=g.getNextValues(g.startState,('move','right'))
ans = g.state[0].getPosition() == n[0].getPosition()
print ans, g.state[0].getPosition(), n[0].getPosition()

print '\n'
