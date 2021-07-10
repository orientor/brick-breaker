from typing import Any
class PowerUp:
    def __init__(self, x, y, icon):
        self.remaining_time: Any=-1
        self.x: Any=x
        self.y: Any=y
        self.v_x: Any=1
        self.icon: Any=icon
    
    def execute(self):
        self.remaining_time: Any=120
        self.x: Any=-1
        self.y: Any=-1
        pass
    
    def deactivate(self):
        pass
    
    def droppowerup(self):
        self.x= self.x + self.v_x

    def reducetime(self):
        self.remaining_time= getattr(self, "remaining_time")-1
