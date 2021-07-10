import global_stuff 
from entity import *
from typing import Any
class paddle(entity):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.length: Any=20
        self.actual_length: Any=20
        self.stick: Any=False
    
    def movepaddle(self, key, balls):
        if key=='d':
            max_d=min(3, global_stuff.cols-getattr(self, "length")-self.y+1)
            self.y+=max_d
            for ball in balls:
                if getattr(ball, "isstuck")():
                    getattr(ball, "movestuckball")(max_d)
        elif key=='a':
            max_d=self.y-max(0, self.y-3)
            self.y-=max_d
            for ball in balls:
                if getattr(ball, "isstuck")():
                    gettattr(ball, "movestuckball")(-max_d)
    
    def increasesize(self):
        self.actual_length+=6
        self.length=max(getattr(self, "actual_length"),2)
    
    def decreasesize(self):
        self.actual_length-=6
        self.length=max(getattr(self, "actual_length"),2)
    
    def get_left_coor(self):
        return getattr(self,"y")
    
    def get_right_coor(self):
        return getattr(self,"y") + self.length
    
    def get_length(self):
        return getattr(self, "length")
    
    def isstick(self):
        return getattr(self, "stick")
