class Visitor(object):
    def __init__(self, name):
        self.name = name
        self.count = 0
        
    def setName(self, name):
        self.name = name
    
    def __call__(self):
        self.count += 1
        return self.name+' called the %sth time.'%(self.count)
        
        