import libdw.sm as sm
class CombLock(sm.SM):
    def __init__(self, keyList):
        self.keyList = keyList
        self.inpList = []

        
    def getNextValues(self, state, inp):
        if inp == 0:
            nextState = 'locked'
            outp = 'locked'
            
        elif inp >= 1 and inp <= 9:
            self.inpList.append(inp)
            nextState = 'locked'
            outp = 'locked'
               
        elif inp == -1:

            if self.inpList == self.keyList:
                nextState = 'unlocked'
                outp = 'unlocked'
                self.inpList = []
            else:
                nextState = 'locked'
                outp = 'locked'
                self.inpList = []

        return nextState, outp
        
l = CombLock([1,2,5])

def mapT2P(x,y):
    if 0 <= x and x <= 3:
        if 0 <= y and y <= 3:
            return 1    
        if 4 <= y and y <= 7:
            return 4
        if 8 <= y and y <= 11:
            return 7
    if 4 <= x and x <= 7:
        if 0 <= y and y <= 3:
            return 2
        if 4 <= y and y <= 7:
            return 5
        if 8 <= y and y <= 11:
            return 8
    if 8 <= x and x <= 11:
        if 0 <= y and y <= 3:
            return 3
        if 4 <= y and y <= 7:
            return 6 
        if 8 <= y and y <= 11:
            return 9
    
class TouchMap(sm.SM):
    
    startState = 0 # Available for touch
    
    def __init__(self):
        self.outp_list = []

    def getNextValues(self, state, inp):
        
        e = inp[0]
        x = inp[1]
        y = inp[2]
        
        if e == 'TouchDown' and state == 0:
            outp = mapT2P(x,y)
            self.outp_list.append(outp)
            nextState = 1 #Finger on screen

        if e == 'TouchUpdate' and state == 1:
            outp = mapT2P(x,y)
            self.outp_list.append(outp)
            if outp == self.outp_list[-2]:
                outp = 0
            nextState = 1
            
        if e == 'TouchUp':
            outp = -1
            nextState = 0
        
        return nextState, outp
        
m=TouchMap()
        